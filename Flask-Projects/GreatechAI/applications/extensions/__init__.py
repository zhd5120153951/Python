from flask import Flask
from .init_login import init_login_manager
from .init_sqlalchemy import init_databases, db, ma


def init_plugs(app: Flask):
    init_login_manager(app)
    init_databases(app)
