from flask import Flask
import os
from app.models.db_engine import db 
from app.jwt_handlers.jwt_init import jwt
# from flask_migrate import Migrate

# migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__,
    instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS"),
            JWT_SECRET_KEY= os.environ.get("JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)
    from app.view.bookmarks import bookmarks
    from app.view.user import auth
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    jwt.init_app(app)
    db.init()
    # migrate.init_app(app, db)
    @app.get('/')
    def index():
        return "Hello!....."
    return app


    