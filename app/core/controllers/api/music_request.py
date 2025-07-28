from flask import request
from ....extensions import db
from ....models.qrcode import MusicRequest, QRCode, DJ, Club, Notification
from ....utils.helpers.user import get_current_user
from ....utils.helpers.http_response import success_response, error_response

class MusicRequestController:
    @staticmethod
    def create():
        """Create a music request or shoutout for a DJ/Club QR code."""
        current_user = get_current_user()
        if not current_user:
            return error_response("Unauthorized", 401)
        data = request.get_json() or {}
        qr_code_id = data.get("qr_code_id")
        req_type = data.get("type")  # 'music_request' or 'shoutout'
        song_title = data.get("song_title")
        message = data.get("message")
        tip_amount = data.get("tip_amount")
        if not qr_code_id or not req_type:
            return error_response("Missing qr_code_id or type", 400)
        qr = QRCode.query.filter_by(id=qr_code_id).first()
        if not qr:
            return error_response("QR code not found", 404)
        dj = qr.dj
        club = qr.club
        music_request = MusicRequest(
            qr_code_id=qr_code_id,
            user_id=current_user.id,
            dj_id=dj.id if dj else None,
            club_id=club.id if club else None,
            type=req_type,
            song_title=song_title,
            message=message,
            tip_amount=tip_amount
        )
        db.session.add(music_request)
        db.session.commit()
        # Create notification for DJ
        if dj:
            notification = Notification(
                dj_id=dj.id,
                music_request_id=music_request.id,
                type=req_type,
                message=message or song_title or "New request"
            )
            db.session.add(notification)
            db.session.commit()
        return success_response("Request submitted", 201, {"request": music_request.to_dict()}) 