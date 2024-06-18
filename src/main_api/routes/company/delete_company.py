import json

from flask import abort, current_app, jsonify, request
from psycopg import OperationalError, ProgrammingError
from pydantic import BaseModel, ValidationError, conint

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/company", methods=["DELETE"])
def delete_company():
    try:
        # Validate the request arguments
        try:
            args = CompanyParams(**request.args.to_dict())
        except ValidationError as e:
            current_app.logger.debug(
                "%s : Validation error in %s", str(e), request.endpoint
            )
            abort(400, description=json.loads(e.json()))

        # Perform delete operation
        db_pool = current_app.config["db_pool"]
        delete_query = """DELETE FROM company WHERE id = %(company_id)s RETURNING id"""
        query_params = {"company_id": args.id}
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_query, query_params)
                if not cursor.fetchone():
                    current_app.logger.debug(
                        "%s : This record does not exist or is referenced by another record in",
                        request.endpoint,
                    )
                    abort(
                        400,
                        description="Delete unsuccessful. This record does not exist or is referenced by another record.",
                    )

        return {"message": "Company record deleted successfully."}
    except (OperationalError, ProgrammingError) as e:
        current_app.logger.error("Server error: %s, %s", request.endpoint, str(e))
        return abort(500, description=json.loads(e.json()))  # Internal Server Error


class CompanyParams(BaseModel):
    id: conint(ge=1)  # type: ignore
