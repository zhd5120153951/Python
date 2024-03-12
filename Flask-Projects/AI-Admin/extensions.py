from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
jwt_manager = JWTManager()


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)

    # 注册一个回调函数
    @jwt_manager.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt_manager.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        # print('user_lookup_callback', _jwt_header, jwt_data)
        identity = jwt_data['sub']
        from models import User
        return User.query.filter_by(id=identity).one_or_none()

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        return {
            redirect('/login')
        }

    @jwt_manager.unauthorized_loader
    def missing_token_callback(error):
        return redirect('/login')
