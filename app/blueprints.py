"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
"""
from typing import List
from flask import Flask, Blueprint

def register_blueprints(app: Flask) -> None:
    
    from .core.routes.api import api_bp, auth_bp, qrcode_bp, template_bp, scan_bp, payment_bp
    from .core.routes.api.admin import admin_api_bp
    
    register_sub_blueprints(api_bp, [auth_bp, qrcode_bp, template_bp, scan_bp, payment_bp, admin_api_bp])
    app.register_blueprint(api_bp)
    
    from .core.routes.debug import debug_bp
    app.register_blueprint(debug_bp)
    
    # Swagger setup
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL: str = '/swagger'
    API_URL: str = '/static/swagger.json'
    swaggerui_blueprint: Blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def register_sub_blueprints(bp: Blueprint, blueprints: List[Blueprint]):
    for sub_bp in blueprints:
        bp.register_blueprint(sub_bp)
