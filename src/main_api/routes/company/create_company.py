import json

from flask import abort, current_app, jsonify, request
from psycopg import OperationalError, ProgrammingError
from pydantic import BaseModel, ValidationError, constr

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/company", methods=["POST"])
def create_company():
    try:
        if not (json_payload := request.get_json(silent=True)):
            abort(400, "Missing JSON In Request")

        # Validate the JSON payload
        try:
            company_data = CompanyInput(**json_payload)
        except ValidationError as e:
            abort(400, json.loads(e.json()))

        # Perform insertion query
        db_pool = current_app.config["db_pool"]
        insert_query = """INSERT INTO company (name) VALUES (%(name)s) RETURNING *"""
        insert_query_params = {"name": company_data.name}
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, insert_query_params)
                if not cursor.fetchone():
                    abort(
                        400,
                        "Cannot insert new company record.",
                    )

        return {"message": "Company record inserted successfully."}

    except (OperationalError, ProgrammingError) as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Bad Request


class CompanyInput(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)  # type: ignore
