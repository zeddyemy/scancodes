from flask import current_app, url_for
from slugify import slugify
from sqlalchemy import inspect

from ..extensions import db
from .user import AppUser, Profile, Address
from .wallet import Wallet
from .role import Role, UserRole
from .qrcode import Template
from ..utils.helpers.loggers import console_log

from ..enums.auth import RoleNames
from ..enums.qrcode import QRCodeType

def create_default_admin(clear: bool = False) -> None:
    
    if inspect(db.engine).has_table("role"):
        admin_role = Role.query.filter_by(name=RoleNames.ADMIN).first()
        admin_role = Role.query.filter_by(name=RoleNames.ADMIN).first()
        
        if not admin_role:
            admin_role = Role(
                name=RoleNames.ADMIN,
                slug=slugify(RoleNames.ADMIN.value)
            )
            db.session.add(admin_role)
            db.session.commit()
        
        if not admin_role:
            admin_role = Role(
                name=RoleNames.ADMIN,
                slug=slugify(RoleNames.ADMIN.value)
            )
            db.session.add(admin_role)
            db.session.commit()
    
    if inspect(db.engine).has_table("app_user"):
        admin = AppUser.query \
                .join(UserRole, AppUser.id == UserRole.app_user_id) \
                .join(Role, UserRole.role_id == Role.id) \
                .filter(Role.name == RoleNames.ADMIN).first()
        
        if clear and admin:
            # Clear existing roles before creating new ones
            admin.delete()
            db.session.close()
            console_log(data="Admin deleted successfully")
            return
        
        if not admin:
            admin_user = AppUser(
                username=current_app.config["DEFAULT_ADMIN_USERNAME"],
                email="admin@admin.com"
            )
            admin_user.password=current_app.config["DEFAULT_ADMIN_PASSWORD"]
            
            admin_user_profile = Profile(firstname="admin", app_user=admin_user)
            admin_user_address = Address(app_user=admin_user)
            admin_user_wallet = Wallet(app_user=admin_user)
            
            db.session.add(admin_user)
            db.session.add_all([admin_user, admin_user_profile, admin_user_address, admin_user_wallet])
            db.session.commit()
            
            admin_user_role = UserRole.assign_role(admin_user, admin_role)
            admin_user_role = UserRole.assign_role(admin_user, admin_role)
            console_log(data="Admin user created with default credentials")
        else:
            console_log(data="Admin user already exists")


def create_roles(clear: bool = False) -> None:
    """Creates default roles if the "role" table doesn't exist.

    Args:
        clear (bool, optional): If True, clears all existing roles before creating new ones. Defaults to False.
    """
    if inspect(db.engine).has_table("role"):
        if clear:
            # Clear existing roles before creating new ones
            Role.query.delete()
            db.session.commit()
        
        for role_name in RoleNames:
            if not Role.query.filter_by(name=role_name).first():
                new_role = Role(name=role_name, slug=slugify(role_name.value))
                db.session.add(new_role)
        db.session.commit()


def create_default_templates(clear: bool = False) -> None:
    """
    Seed the database with default QR code templates if none exist.
    Args:
        clear (bool): If True, clear all existing templates before seeding.
    """
    from .qrcode import Template
    from ..enums.qrcode import QRCodeType
    from sqlalchemy import inspect
    if inspect(db.engine).has_table("template"):
        if clear:
            Template.query.delete()
            db.session.commit()
        if Template.query.count() == 0:
            templates = [
                Template(
                    name="Restaurant Menu",
                    type=str(QRCodeType.MENU),
                    schema_definition={"url": "string", "restaurant_name": "string", "table_number": "string"},
                    preview_url="https://…/menu_thumb.png",
                    description="A template for restaurant menus with table numbers."
                ),
                Template(
                    name="Business Card",
                    type=str(QRCodeType.CARD),
                    schema_definition={"name": "string", "title": "string", "company": "string", "phone": "string", "email": "string"},
                    preview_url="https://…/card_thumb.png",
                    description="A template for digital business cards."
                ),
                Template(
                    name="Club DJ",
                    type="club_dj",
                    schema_definition={"club_id": "integer", "dj_id": "integer"},
                    preview_url="https://…/club_dj_thumb.png",
                    description="A template for DJs working under a club."
                ),
                Template(
                    name="Personal DJ",
                    type="personal_dj",
                    schema_definition={"dj_id": "integer"},
                    preview_url="https://…/personal_dj_thumb.png",
                    description="A template for personal DJs."
                ),
            ]
            db.session.add_all(templates)
            db.session.commit()

