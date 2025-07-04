"""
This package contains the database models for the Flask application.

It includes models for User, Product, Category, Role, etc. Each model corresponds to a table in the database.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: GNU, see LICENSE for more details.
Package: StoreZed
"""
from flask import Flask
from sqlalchemy.orm import aliased

from .media import Media
from .user import AppUser, Profile, Address, TempUser
from .role import Role, UserRole,  user_roles
from .wallet import Wallet

from .payment import Payment, Transaction
from .subscription import Subscription, SubscriptionPlan
from .defaults import create_default_admin, create_roles


def create_db_defaults(app: Flask) -> None:
    with app.app_context():
        create_roles()
        create_default_admin()