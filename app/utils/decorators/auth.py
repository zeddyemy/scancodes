'''
This module defines the `roles_required` decorator for the Flask application.

Used for handling role-based access control.
The `roles_required` decorator is used to ensure that the current user has all of the specified roles.
If the user does not have the required roles, it returns a 403 error.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
Package: BitnShop
'''
from functools import wraps
from typing import Callable, TypeVar, Tuple, Any, Union
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app,  request, redirect, flash, url_for, render_template, Response
from flask.typing import ResponseReturnValue
from flask_login import LoginManager, login_required, current_user as session_user

from app.models import AppUser
from app.extensions import db
from ..helpers.loggers import console_log
from ..helpers.http_response import error_response
from ..helpers.user import get_current_user
from ..helpers.roles import normalize_role

# Define type variables for better type hinting
F = TypeVar('F', bound=Callable[..., Any])

def roles_required(*required_roles: str) -> Callable[[F], F]:
    """
    Decorator to ensure that the current user has all of the specified roles.

    This decorator will return a 403 error if the current user does not have
    all of the roles specified in `required_roles`.

    Args:
        *required_roles (str): The required roles to access the route.

    Returns:
        function: The decorated function.

    Raises:
        HTTPException: A 403 error if the current user does not have the required roles.
    """
    
    normalized_required_roles = {normalize_role(role) for role in required_roles}
    
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = get_current_user()
            
            if not current_user:
                return error_response("Unauthorized", 401)
            
            if not any(normalize_role(user_role.role.name.value) in normalized_required_roles 
                        for user_role in current_user.roles):
                return error_response("Access denied: Insufficient permissions", 403)
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
