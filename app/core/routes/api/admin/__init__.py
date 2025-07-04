from flask import Blueprint

admin_api_bp: Blueprint = Blueprint('admin_api', __name__, url_prefix='/admin')