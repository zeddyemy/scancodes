"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
"""
from flask import Blueprint

api_bp: Blueprint = Blueprint('api', __name__, url_prefix='/api')

from .base import auth, index