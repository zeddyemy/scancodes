from .. import api_bp
from ....controllers.api import BaseController

@api_bp.route("/payments", methods=["GET", "POST", "PUT", "DELETE"])
def manage_payments():
    """
    Returns basic site information from settings.
    """
    return BaseController.site_info()