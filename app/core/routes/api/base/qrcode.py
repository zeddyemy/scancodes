from flask import Blueprint, request

from .. import api_bp
from ....controllers.api import QrCodeController
from .....utils.decorators.auth import roles_required

qrcode_bp = Blueprint('qrcode', __name__, url_prefix='/qrcodes')
api_bp.register_blueprint(qrcode_bp)

@qrcode_bp.route("/", methods=["GET", "PUT", "DELETE"])
def qrcode():
    if request.method == "GET":
        return QrCodeController.list()
    elif request.method == "POST":
        return QrCodeController.create()

@qrcode_bp.route("/<int:id>", methods=["GET", "DELETE"])
def manage_qrcode(id):
    if request.method == "GET":
        return QrCodeController.get(id)
    elif request.method == "DELETE":
        return QrCodeController.delete(id)

