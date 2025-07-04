from flask_login import current_user

from .utils.helpers.loggers import console_log
from .utils.helpers.user import get_app_user_info
from .extensions import db

def app_context_Processor():
    user_id = current_user.id if current_user.is_authenticated else None
    
    current_user_info = get_app_user_info(user_id)
    
    
    return {
        'CURRENT_USER': current_user_info,
        'SITE_INFO': {
            "site_title": "ScanCodes",
            "site_tagline": "Business first logic",
            "currency": "NGN",
        },
    }