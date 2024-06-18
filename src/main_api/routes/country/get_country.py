import json

from flask import abort, current_app, request
from psycopg import OperationalError, ProgrammingError

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/country")
def get_country():
    try:
        db_pool = current_app.config["db_pool"]
        query = "SELECT ARRAY_AGG(name) AS countries FROM country"
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                companies = cursor.fetchone()

        if not companies:
            current_app.logger.debug(
                "No country records were found at %s", request.endpoint
            )
            abort(404, description="No country records were found.")

        return companies

    except (OperationalError, ProgrammingError) as e:
        abort(500, description=json.loads(e.json()))  # Internal Server Error
