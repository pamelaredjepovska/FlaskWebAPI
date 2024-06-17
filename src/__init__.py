import psycopg
from flask import Flask, app
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    """Create and configure the Flask app

    Returns:
        app (Flask): Flask app
    """

    # Create a Flask app instance and apply app config
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Register blueprints
    register_main_api(app)
    register_swagger(app)

    return app


def register_main_api(app: Flask) -> None:
    from src.main_api import main_api_blueprint

    app.register_blueprint(main_api_blueprint, url_prefix="/main_api")


def register_swagger(app: Flask) -> None:
    from .swagger import swagger_config

    swagger_config(app)

    SWAGGER_URL = app.config["SWAGGER_URL"]
    SWAGGER_API_URL = app.config["SWAGGER_API_URL"]
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, SWAGGER_API_URL, config={"app_name": "Flask Web API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def get_db_connection():
    conn = psycopg.connect(app.config["DATABASE_URL"])
    return conn
