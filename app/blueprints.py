"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
"""

from flask import Flask, Blueprint

def register_all_blueprints(app: Flask) -> None:
    
    from .core.routes.api import api_bp
    from .core.routes.api.admin import admin_api_bp
    api_bp.register_blueprint(admin_api_bp)
    app.register_blueprint(api_bp)
    
    from .core.routes.debug import debug_bp
    app.register_blueprint(debug_bp)
    
    # Swagger setup
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL: str = '/swagger'
    API_URL: str = '/static/swagger.json'
    swaggerui_blueprint: Blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
