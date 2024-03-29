from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from WebApp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()
loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(hours=1)

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    from WebApp.users.routes import users
    from WebApp.main.routes import main
    from WebApp.rooms.routes import rooms
    from WebApp.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(rooms)
    app.register_blueprint(errors)

    return app
