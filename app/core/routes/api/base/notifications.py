from flask import Blueprint, request
from .. import api_bp
from ....controllers.api.notification import NotificationController

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')
api_bp.register_blueprint(notifications_bp)

@notifications_bp.route('/', methods=['GET'])
def list_notifications():
    """List notifications for the current DJ (by user)."""
    return NotificationController.list() 