from flask import request
from ....extensions import db
from ....models.qrcode import Notification, DJ
from ....utils.helpers.user import get_current_user
from ....utils.helpers.http_response import success_response, error_response

class NotificationController:
    @staticmethod
    def list():
        """List notifications for the current DJ (by user)."""
        current_user = get_current_user()
        if not current_user:
            return error_response("Unauthorized", 401)
        # Find DJ profile for this user
        dj = DJ.query.filter_by(user_id=current_user.id).first()
        if not dj:
            return error_response("No DJ profile found for user", 404)
        notifications = Notification.query.filter_by(dj_id=dj.id).order_by(Notification.created_at.desc()).all()
        return success_response("Notifications fetched", 200, {"notifications": [n.to_dict() for n in notifications]}) 