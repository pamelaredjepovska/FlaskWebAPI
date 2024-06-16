import psycopg
from flask import Flask, app
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from .main_api.routes.health_check import main_api

    app.register_blueprint(main_api, url_prefix="/main_api")

    from .swagger import swagger_config

    swagger_config(app)

    SWAGGER_URL = app.config["SWAGGER_URL"]
    SWAGGER_API_URL = app.config["SWAGGER_API_URL"]
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, SWAGGER_API_URL, config={"app_name": "Flask Web API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app


def get_db_connection():
    conn = psycopg.connect(app.config["DATABASE_URL"])
    return conn
