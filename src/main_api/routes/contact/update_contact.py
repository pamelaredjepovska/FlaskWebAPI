import json
from typing import Optional

from flask import abort, current_app, request
from psycopg import OperationalError, ProgrammingError, sql
from pydantic import BaseModel, ValidationError, conint, constr

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/contact", methods=["PATCH"])
def update_contact():
    try:
        if not (json_payload := request.get_json(silent=True)):
            abort(400, description="Missing JSON In Request")

        # Validate the request arguments and JSON payload
        try:
            args = ContactParams(**request.args.to_dict())
            contact_data = ContactInput(**json_payload)
        except ValidationError as e:
            current_app.logger.debug(
                "%s : Validation error in %s", str(e), request.endpoint
            )
            abort(400, description=json.loads(e.json()))

        print(f"contact_data = {contact_data}")
        # Perform update query
        db_pool = current_app.config["db_pool"]
        update_query = (
            """UPDATE contact SET {set_clause} WHERE id = %(contact_id)s RETURNING *"""
        )
        # Build the SET clause dynamically
        set_clauses = []
        update_query_params = {"contact_id": args.id}

        for key, value in contact_data.model_dump().items():
            if value is not None:  # Only include non-None values
                if key == "name":
                    set_clauses.append("name = %(name)s")
                    update_query_params["name"] = value
                elif key == "country":
                    set_clauses.append(
                        "country_id = (SELECT id FROM country WHERE name = %(country)s)"
                    )
                    update_query_params["country"] = value
                elif key == "company":
                    set_clauses.append(
                        "company_id = (SELECT id FROM company WHERE name = %(company)s)"
                    )
                    update_query_params["company"] = value

        # If no valid fields are provided for update
        if not set_clauses:
            abort(400, description="No valid fields to update.")

        # Format the query with the final set clause
        set_clause = ", ".join(set_clauses)
        update_query = sql.SQL(
            """UPDATE contact SET {set_clause} WHERE id = %(contact_id)s RETURNING *"""
        ).format(set_clause=sql.SQL(set_clause))

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

        return {"message": "Contact record updated successfully."}
    except (OperationalError, ProgrammingError) as e:
        current_app.logger.error("Server error: %s, %s", request.endpoint, str(e))
        return abort(500, description=json.loads(e.json()))  # Internal Server Error


class ContactParams(BaseModel):
    id: conint(ge=1)  # type: ignore


class ContactInput(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1)] = None  # type: ignore
    country: Optional[constr(strip_whitespace=True, min_length=1)] = None  # type: ignore
    company: Optional[constr(strip_whitespace=True, min_length=1)] = None  # type: ignore
