'''
This module defines the routes for authentication operations in the Flask application.

It includes routes for signing up, verifying email, logging in, verifying 2FA, forgetting password, and resetting password.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
'''
from flask import request
from flask_jwt_extended import jwt_required

from .. import api_bp
from ....controllers.api import AuthController


# REGISTRATION ENDPOINTS
@api_bp.route("/auth/signup", methods=["POST"])
def signUp():
    return AuthController.signUp()

# AUTHENTICATION ENDPOINTS
@api_bp.route("/auth/login", methods=["POST"])
def login():
    return AuthController.login()