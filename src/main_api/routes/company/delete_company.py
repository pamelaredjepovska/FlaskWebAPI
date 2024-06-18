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
            abort(400, json.loads(e.json()))

        # Perform delete operation
        db_pool = current_app.config["db_pool"]
        delete_query = """DELETE FROM company WHERE id = %(company_id)s RETURNING id"""
        query_params = {"company_id": args.id}
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_query, query_params)
                if not cursor.fetchone():
                    abort(
                        400,
                        "Delete unsuccessful. This record does not exist or is referenced by another record.",
                    )

        return {"message": "Company record deleted successfully."}
    except (OperationalError, ProgrammingError) as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Bad Request


class CompanyParams(BaseModel):
    id: conint(ge=1)  # type: ignore
