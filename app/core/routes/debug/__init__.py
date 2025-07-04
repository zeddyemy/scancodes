"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
"""

from flask import Blueprint, render_template

debug_bp: Blueprint = Blueprint('dev_debug', __name__, url_prefix='/dev/debug')

from . import cookies