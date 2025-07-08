from .. import payment_bp
from ....controllers.api import BaseController

@payment_bp.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def manage_payments():
    """
    Returns basic site information from settings.
    """
    return BaseController.site_info()