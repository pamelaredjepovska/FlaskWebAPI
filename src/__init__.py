from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from src.errors import register_error_handlers
from src.logger import setup_logging


def create_app():
    """Create and configure the Flask app

    Returns:
        app (Flask): Flask app
    """

    # Create a Flask app instance and apply app config
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Setup logging
    logger = setup_logging()
    app.logger.addHandler(logger)
    app.logger.debug(
        "App logger initialized"
    )  # Debug message to ensure logger is initialized

    # Register blueprints
    register_main_api(app)
    register_swagger(app)

    # Register error handlers
    register_error_handlers(app)

    app.config.update({"db_pool": initialize_db_pool(app)})

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


def get_db_connection(db_pool: ConnectionPool):
    return db_pool.connection()


def initialize_db_pool(app: Flask) -> ConnectionPool:
    """
    Create an instance of a threaded psycopg3 pool.
    https://www.psycopg.org/psycopg3/docs/api/pool.html#psycopg_pool.ConnectionPool
    """

    conninfo = make_conninfo(
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        host=app.config["DB_HOST"],
        port=5432,
        dbname=app.config["DB_NAME"],
    )

    # return psycopg3 database pool instance
    return ConnectionPool(
        conninfo=conninfo,
        min_size=app.config.get("DB_POOL_MIN_CONN", 1),
        max_size=app.config.get("DB_POOL_MAX_CONN", 2),
        kwargs={"row_factory": dict_row},
    )
