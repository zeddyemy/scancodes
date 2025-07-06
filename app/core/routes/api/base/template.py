from flask import Blueprint, request

from ....controllers.api.template import TemplateController
from .. import api_bp

template_bp = Blueprint('template', __name__, url_prefix='/templates')
api_bp.register_blueprint(template_bp)

@template_bp.route("/", methods=["GET", "POST"])
def manage_templates():
    if request.method == "GET":
        return TemplateController.get_templates()
    elif request.method == "POST":
        return TemplateController.create()