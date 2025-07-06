from flask import render_template

from ....utils.helpers.http_response import error_response, success_response
from ....utils.helpers.loggers import log_exception, console_log

class BaseController:
    @staticmethod
    def index():
        """
        Returns html template
        """
        return render_template("api/index.html")
    
    @staticmethod
    def site_info():
        return success_response("Successful Response", 200)