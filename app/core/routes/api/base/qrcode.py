from flask import Blueprint, request

from ....controllers.api import QrCodeController
from .....utils.decorators.auth import roles_required

qrcode_bp = Blueprint('qrcode', __name__, url_prefix='/qrcodes')

@qrcode_bp.route("/", methods=["GET", "PUT", "DELETE"])
@roles_required("Admin, Customer")
def qrcode():
    if request.method == "GET":
        return QrCodeController.get_qrcodes()
    elif request.method == "POST":
        return QrCodeController.create()

