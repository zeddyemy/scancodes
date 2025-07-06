# app/core/controllers/api/template.py
from typing import List

from ....extensions import db
from ....models.template import Template
from ....utils.helpers.http_response import success_response

class TemplateController:
    @staticmethod
    def get_templates():
        templates: List[Template] = Template.query.all()
        
        data  = {
            "templates": [t.to_dict() for t in templates]
        }
        return success_response("Templates fetched successfully", 200, data)
