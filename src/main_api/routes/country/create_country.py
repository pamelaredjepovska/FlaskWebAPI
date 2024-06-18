import json

from flask import abort, current_app, jsonify, request
from psycopg import OperationalError, ProgrammingError
from pydantic import BaseModel, ValidationError, constr

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/country", methods=["POST"])
def create_country():
    try:
        if not (json_payload := request.get_json(silent=True)):
            abort(400, description="Missing JSON In Request")

        # Validate the JSON payload
        try:
            country_data = CountryInput(**json_payload)
        except ValidationError as e:
            current_app.logger.debug(
                "%s : Validation error in %s", str(e), request.endpoint
            )
            abort(400, description=json.loads(e.json()))

        # Perform insertion query
        db_pool = current_app.config["db_pool"]
        insert_query = """INSERT INTO country (name) VALUES (%(name)s) RETURNING *"""
        insert_query_params = {"name": country_data.name}
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, insert_query_params)

        return {"message": "Country record inserted successfully."}

    except (OperationalError, ProgrammingError) as e:
        current_app.logger.error("Server error: %s, %s", request.endpoint, str(e))
        return abort(500, description=json.loads(e.json()))  # Internal Server Error


class CountryInput(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)  # type: ignore
