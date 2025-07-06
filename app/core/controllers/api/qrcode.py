from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ....extensions import db
from ....models.qrcode import QRCode
from ....utils.helpers.http_response import success_response, error_response
from ....utils.helpers.qrcode import make_qr, store_qr
from ....enums.qrcode import QRCodeType

class QrCodeController:
    @staticmethod
    def create():
        data    = request.get_json() or {}
        typ     = data.get("type")
        payload = data.get("payload")
        if not (typ and payload):
            return error_response("`type` and `payload` required", 400)

        # validate type
        try:
            typ_enum = QRCodeType(typ)
        except ValueError:
            return error_response("Invalid QR code type", 400)

        # generate & store
        buf = make_qr(payload)
        url = store_qr(buf)

        user_id = get_jwt_identity()
        qr      = QRCode(user_id=user_id, type=str(typ_enum), payload=payload, image_url=url)
        db.session.add(qr)
        db.session.commit()

        return success_response("QR code created", 201, {"qrcode": qr.to_dict()})

    @staticmethod
    def list():
        user_id = get_jwt_identity()
        items   = QRCode.query.filter_by(user_id=user_id).all()
        return success_response(
            "QR codes fetched",
            200,
            {"qrcodes": [qr.to_dict() for qr in items]},
        )

    @staticmethod
    def get(id: int):
        user_id = get_jwt_identity()
        qr      = QRCode.query.filter_by(id=id, user_id=user_id).first()
        if not qr:
            return error_response("Not found", 404)
        return success_response("QR code fetched", 200, {"qrcode": qr.to_dict()})

    @staticmethod
    def delete(id: int):
        user_id = get_jwt_identity()
        qr      = QRCode.query.filter_by(id=id, user_id=user_id).first()
        if not qr:
            return error_response("Not found", 404)

        db.session.delete(qr)
        db.session.commit()
        return success_response("QR code deleted", 200, None)
