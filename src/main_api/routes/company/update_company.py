import json

from flask import abort, current_app, jsonify, request
from psycopg import OperationalError, ProgrammingError
from pydantic import BaseModel, ValidationError, conint, constr

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/company", methods=["PATCH"])
def update_company():
    try:
        if not (json_payload := request.get_json(silent=True)):
            abort(400, description="Missing JSON In Request")

        # Validate the request arguments and JSON payload
        try:
            args = CompanyParams(**request.args.to_dict())
            company_data = CompanyInput(**json_payload)
        except ValidationError as e:
            current_app.logger.debug(
                "%s : Validation error in %s", str(e), request.endpoint
            )
            abort(400, description=json.loads(e.json()))

        # Perform update query
        db_pool = current_app.config["db_pool"]
        update_query = """UPDATE company SET name = %(name)s WHERE id = %(company_id)s RETURNING *"""
        update_query_params = {"name": company_data.name, "company_id": args.id}
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(update_query, update_query_params)
                update_result = cursor.fetchone()

                # If there is not record with that ID, abort the operation
                if not update_result:
                    current_app.logger.debug(
                        "%s : No record found with given ID in", request.endpoint
                    )
                    abort(400, description="The record does not exist.")

        return {"message": "Company record updated successfully."}
    except (OperationalError, ProgrammingError) as e:
        current_app.logger.error("Server error: %s, %s", request.endpoint, str(e))
        return abort(500, description=json.loads(e.json()))  # Internal Server Error


class CompanyParams(BaseModel):
    id: conint(ge=1)  # type: ignore


class CompanyInput(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)  # type: ignore
