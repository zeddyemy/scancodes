"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
"""
from flask import Blueprint

api_bp: Blueprint = Blueprint('api', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
template_bp = Blueprint('template', __name__, url_prefix='/templates')
qrcode_bp = Blueprint('qrcode', __name__, url_prefix='/qrcodes')
scan_bp = Blueprint('scan', __name__, url_prefix='/scan')
payment_bp = Blueprint('payment', __name__, url_prefix='/payments')

from .base import index, auth, qrcode, template, payment