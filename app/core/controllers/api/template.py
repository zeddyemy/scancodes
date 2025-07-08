# app/core/controllers/api/template.py
from typing import List

from ....extensions import db
from ....models.qrcode import Template
from ....utils.helpers.http_response import success_response

class TemplateController:
    @staticmethod
    def get_templates():
        """Fetch all available QR code templates."""
        templates: List[Template] = Template.query.all()
        
        data  = {
            "templates": [t.to_dict() for t in templates]
        }
        return success_response("Templates fetched successfully", 200, data)

    @staticmethod
    def create():
        """Stub for creating a new template (not implemented)."""
        return success_response("Not implemented", 501)
