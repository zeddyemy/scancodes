from flask import render_template

from .. import api_bp
from ....controllers.api import BaseController


@api_bp.route("/", methods=["GET"])
def index():
    return BaseController.index()

@api_bp.route("/info")
def site_info():
    """
    Returns basic site information from settings.
    """
    return BaseController.site_info()