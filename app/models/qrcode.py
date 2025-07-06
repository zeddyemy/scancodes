from datetime import datetime
from ..extensions import db
from ..enums.qrcode import QRCodeType
from ..utils.date_time import DateTimeUtils, to_gmt1_or_none

class QRCode(db.Model):
    __tablename__ = "qr_code"

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    type         = db.Column(db.Enum(QRCodeType), nullable=False)
    payload      = db.Column(db.Text, nullable=False)
    image_url    = db.Column(db.String(512), nullable=False)
    host_expires = db.Column(db.DateTime(timezone=True), nullable=True)
    wallet_id    = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=True)

    created_at   = db.Column(db.DateTime(timezone=True), default=DateTimeUtils.aware_utcnow)
    updated_at   = db.Column(db.DateTime(timezone=True), default=DateTimeUtils.aware_utcnow, onupdate=DateTimeUtils.aware_utcnow)

    app_user   = db.relationship('AppUser', back_populates='qrcodes')
    wallet = db.relationship('Wallet', back_populates='qrcodes')
    
    def __repr__(self) -> str:
        return f"<QRCode {self.id}, Type: {self.type}>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'type': self.type,
            'payload': self.payload,
            'image_url': self.image_url,
            'created_at': to_gmt1_or_none(self.created_at),
            'updated_at': to_gmt1_or_none(self.updated_at),
        }
