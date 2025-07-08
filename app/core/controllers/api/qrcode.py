from uuid import uuid4
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ....extensions import db
from ....models.qrcode import QRCode, Template
from ....utils.helpers.loggers import console_log
from ....utils.helpers.validate import validate_json_data
from ....utils.helpers.user import get_current_user
from ....utils.helpers.http_response import success_response, error_response
from ....utils.helpers.qr_generator import generate_qr_code_image
from ....utils.helpers.cloudinary_uploader import upload_qr_code_to_cloudinary, delete_qr_code_from_cloudinary
from ....enums.qrcode import QRCodeType

class QrCodeController:
    @staticmethod
    def create():
        """Create a new QR code for the current user, validating data against the template schema and uploading the image to Cloudinary."""
        current_user = get_current_user()
        if not current_user:
            return error_response("Unauthorized", 401)
        data = request.get_json() or {}
        template_id = data.get("template_id")
        temp_type = data.get("type")
        payload = data.get("data")
        if not data or not template_id or not payload:
            return error_response("Missing template_id or data", 400)
        template = Template.query.get(template_id)
        if not template:
            console_log("MSG", f"Template with ID {template_id} not found.", "WARNING")
            return error_response("Template not found", 404)
        if not validate_json_data(payload, template.schema_definition):
            console_log("Warning", f"Data payload for template {template_id} does not match schema.", "WARNING")
            return error_response("Data payload does not match template schema", 400)
        if temp_type:
            try:
                typ_enum = QRCodeType(temp_type)
            except ValueError:
                return error_response("Invalid QR code type", 400)
        try:
            new_qr_code_uuid = str(uuid4())
            public_scan_url = (
                f"{current_app.config['FRONTEND_BASE_URL']}/"
                f"{current_user.short_code}/"
                f"{template.name}/"
                f"{new_qr_code_uuid}"
            )
            qr_image_stream, mime_type = generate_qr_code_image(public_scan_url)
            qr_code_image_url = upload_qr_code_to_cloudinary(qr_image_stream, new_qr_code_uuid)
            new_qr = QRCode(
                id=new_qr_code_uuid,
                user_id=current_user.id,
                template_id=template_id,
                data_payload=payload,
                qr_code_image_url=qr_code_image_url,
                type=temp_type
            )
            db.session.add(new_qr)
            db.session.commit()
            current_app.logger.info(f"QR Code {new_qr_code_uuid} created for user {current_user.id}.")
            return success_response(
                "QR code created",
                201,
                {
                    "qr_code_id": new_qr.id,
                    "qr_code_image_url": new_qr.qr_code_image_url,
                    "public_scan_url": public_scan_url
                }
            )
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating QR code for user {current_user.id}: {e}")
            if 'qr_code_image_url' in locals() and qr_code_image_url:
                delete_qr_code_from_cloudinary(new_qr_code_uuid)
                current_app.logger.warning(f"Cleaned up Cloudinary for failed QR code {new_qr_code_uuid}.")
            return error_response("Internal server error during QR code creation", 500)

    @staticmethod
    def list():
        """List all QR codes for the current user."""
        user_id = get_jwt_identity()
        items = QRCode.query.filter_by(user_id=user_id).all()
        return success_response(
            "QR codes fetched",
            200,
            {"qrcodes": [qr.to_dict() for qr in items]},
        )

    @staticmethod
    def get(id: int):
        """Get a specific QR code by ID for the current user."""
        user_id = get_jwt_identity()
        qr = QRCode.query.filter_by(id=id, user_id=user_id).first()
        if not qr:
            return error_response("Not found", 404)
        return success_response("QR code fetched", 200, {"qrcode": qr.to_dict()})

    @staticmethod
    def delete(id: int):
        """Delete a specific QR code by ID for the current user."""
        user_id = get_jwt_identity()
        qr = QRCode.query.filter_by(id=id, user_id=user_id).first()
        if not qr:
            return error_response("Not found", 404)
        db.session.delete(qr)
        db.session.commit()
        return success_response("QR code deleted", 200, None)
