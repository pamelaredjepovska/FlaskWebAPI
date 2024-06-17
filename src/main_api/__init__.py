from flask import Blueprint, g
from werkzeug.utils import find_modules, import_string

from src import get_db_connection

main_api_blueprint = Blueprint("main_api", __name__)


# Standard blueprint for all the main API routes
@main_api_blueprint.before_request
def main_api_routes():
    g.conn = get_db_connection()


@main_api_blueprint.teardown_request
def main_api_teardown(exception=None):
    conn = getattr(g, "conn", None)
    print(f"conn = {conn}")
    if conn is not None:
        conn.close()


# Make all the route modules directly importable
for module in find_modules("src.main_api.routes", recursive=True):
    import_string(module)
