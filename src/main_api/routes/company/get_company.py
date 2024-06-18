from flask import current_app, jsonify
from psycopg import OperationalError, ProgrammingError

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/company")
def get_company():
    try:
        db_pool = current_app.config["db_pool"]
        query = "SELECT ARRAY_AGG(name) AS companies FROM company"
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                companies = cursor.fetchone()

        if not companies:
            return jsonify({"error": "No companies found"}), 404  # Not Found

        return companies

    except (OperationalError, ProgrammingError) as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Bad Request
