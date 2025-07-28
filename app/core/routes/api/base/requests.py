from flask import Blueprint, request
from .. import api_bp
from ....controllers.api.music_request import MusicRequestController

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')
api_bp.register_blueprint(requests_bp)

@requests_bp.route('/', methods=['POST'])
def create_request():
    """Create a music request or shoutout for a DJ/Club QR code."""
    return MusicRequestController.create() 