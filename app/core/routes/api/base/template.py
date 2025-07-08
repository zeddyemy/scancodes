from flask import Blueprint, request

from ....controllers.api.template import TemplateController
from .. import template_bp

@template_bp.route("/", methods=["GET", "POST"])
def manage_templates():
    """Handle GET (list templates) and POST (create template, not implemented) requests."""
    if request.method == "GET":
        return TemplateController.get_templates()
    elif request.method == "POST":
        return TemplateController.create()