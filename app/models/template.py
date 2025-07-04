'''
This module defines the Template model for the database.

@author Emmanuel Olowu
@link: https://github.com/zeddyemy
'''

from ..extensions import db

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))