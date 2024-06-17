from flask import Blueprint, g
from werkzeug.utils import find_modules, import_string

main_api_blueprint = Blueprint("main_api", __name__)


# Standard blueprint for all the main API routes
@main_api_blueprint.before_request
def main_api_routes():
    pass


# Make all the route modules directly importable
for module in find_modules("src.main_api.routes", recursive=True):
    import_string(module)
