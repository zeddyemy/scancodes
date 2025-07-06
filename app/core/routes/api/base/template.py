from .. import api_bp
from ....controllers.api import BaseController

@api_bp.route("/templates", methods=["GET", "POST", "PUT", "DELETE"])
def manage_templates():
    """
    Returns basic site information from settings.
    """
    return BaseController.site_info()