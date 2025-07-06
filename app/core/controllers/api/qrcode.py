from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ....extensions import db
from ....models.qrcode import QRCode
from ....utils.helpers.qrcode import make_qr, store_qr
from ....utils.helpers.http_response import success_response, error_response

class QrCodeController:
    @staticmethod
    @jwt_required()
    def create():
        data = request.get_json() or {}
        qr_type = data.get("type")
        payload = data.get("payload")
        if not (qr_type and payload):
            return error_response("type & payload required", 400)

        img_buf = make_qr(payload)
        url     = store_qr(img_buf)
        user_id = get_jwt_identity()

        qr:QRCode = QRCode(user_id=user_id, type=qr_type, payload=payload, image_url=url)
        db.session.add(qr)
        db.session.commit()
        return success_response("QR created", 201, qr.to_dict())
