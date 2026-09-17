from flask import Flask

from app.extensions import db
from config import Config, get_database_uri
from app.routes.products import products_bp
from app.routes.general import general_bp

from app.errors.handlers import register_error_handlers


def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri(config)

    db.init_app(app)

    app.register_blueprint(products_bp)
    app.register_blueprint(general_bp)

    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
