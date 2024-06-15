import psycopg
from flask import Flask, app


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from .main_api.routes.health_check import main_api

    app.register_blueprint(main_api, url_prefix="/main_api")

    return app


def get_db_connection():
    conn = psycopg.connect(app.config["DATABASE_URL"])
    return conn
