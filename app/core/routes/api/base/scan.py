from flask import Blueprint, request

from .. import scan_bp
from ....controllers.api import QrCodeController
from .....utils.decorators.auth import roles_required

@scan_bp.route("/<string:short_code>/<string:template_type>/<uuid:uuid>", methods=["GET", "POST"])
def scan(short_code, template_type, uuid):
    """Scan endpoint: fetch QR code by uuid, validate short_code and template_type, and return data."""
    from .....models.qrcode import QRCode, Template
    from .....models.user import AppUser
    qr = QRCode.query.filter_by(id=str(uuid)).first()
    if not qr:
        return {"message": "QR code not found"}, 404
    user = AppUser.query.filter_by(unique_code=short_code).first()
    if not user or user.id != qr.user_id:
        return {"message": "Invalid user for this QR code"}, 404
    template = Template.query.filter_by(id=qr.template_id).first()
    if not template or template.type != template_type:
        return {"message": "Invalid template for this QR code"}, 404
    return {"data": qr.to_dict()}, 200