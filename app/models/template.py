'''
This module defines the Template model for the database.

@author Emmanuel Olowu
@link: https://github.com/zeddyemy
'''

from ..extensions import db
from ..enums.qrcode import QRCodeType

class Template(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String, nullable=False)
    type           = db.Column(db.String(150), nullable=False)
    payload_schema = db.Column(db.JSON, nullable=False)
    preview_url    = db.Column(db.String)
    
    def __repr__(self) -> str:
        return f"<Template {self.id}, Type: {self.type}>"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'payload_schema': self.payload_schema,
            'preview_url': self.preview_url,
        }

