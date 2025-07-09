from flask import Blueprint, request

from .. import qrcode_bp
from ....controllers.api import QrCodeController
from .....utils.decorators.auth import roles_required

@qrcode_bp.route("/", methods=["GET", "POST"])
@roles_required("Admin", "Customer")
def qrcode():
    if request.method == "GET":
        return QrCodeController.list()
    elif request.method == "POST":
        return QrCodeController.create()

@qrcode_bp.route("/<string:id>", methods=["GET", "PUT", "DELETE"])
@roles_required("Admin", "Customer")
def manage_qrcode(id):
    """Get, update, or delete a specific QR code by ID."""
    if request.method == "GET":
        return QrCodeController.get(id)
    elif request.method == "PUT":
        return QrCodeController.update(id)
    elif request.method == "DELETE":
        return QrCodeController.delete(id)

