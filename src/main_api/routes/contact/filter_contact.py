import json
from typing import Optional

from flask import abort, current_app, request
from psycopg import OperationalError, ProgrammingError, sql
from pydantic import BaseModel, ValidationError, constr

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/contact/filter")
def filter_contact():
    try:
        # Validate the request arguments
        try:
            args = FilterContactParams(**request.args.to_dict())
        except ValidationError as e:
            current_app.logger.debug(
                "%s : Validation error in %s", str(e), request.endpoint
            )
            abort(400, description=json.loads(e.json()))

        # Build the WHERE clause dynamically
        where_clauses = []
        filter_query_params = {}

        for key, value in args.model_dump().items():
            # Only include non-None values
            if value is not None:
                column_name = f"{key}_id"
                table_name = key
                column_value = f"{key}_value"
                where_clauses.append(
                    sql.SQL(
                        "{column_name} = (SELECT id FROM {table_name} WHERE name = {column_value})"
                    ).format(
                        column_name=sql.Identifier(column_name),
                        table_name=sql.Identifier(table_name),
                        column_value=sql.Placeholder(column_value),
                    )
                )
                filter_query_params[column_value] = value

        # If no valid fields are provided for filtering
        if not where_clauses:
            abort(400, description="No filter has been aplied.")

        # Format the query with the final where clause
        where_clause = sql.SQL(" OR ").join(where_clauses)
        filter_query = sql.SQL(
            """SELECT json_agg(
                        json_build_object(
                            'id', contact.id,
                            'name', contact.name,
                            'country', country.name,
                            'company', company.name
                        )
                ) AS contacts
                FROM 
                    contact
                JOIN 
                    country ON contact.country_id = country.id
                JOIN 
                    company ON contact.company_id = company.id
                WHERE {where_clause}"""
        ).format(where_clause=where_clause)

        db_pool = current_app.config["db_pool"]
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(filter_query, filter_query_params)
                filtered_contacts = cursor.fetchall()

                # If there are no records with the requested filter(s), abort
                if not filtered_contacts[0]["contacts"]:
                    current_app.logger.debug(
                        "No contact records were found at %s", request.endpoint
                    )
                    abort(
                        404,
                        description="No contact records were found for the specified filter.",
                    )

        return filtered_contacts
    except (OperationalError, ProgrammingError) as e:
        current_app.logger.error("Server error: %s, %s", request.endpoint, str(e))
        return abort(500, description=json.loads(e.json()))  # Internal Server Error


class FilterContactParams(BaseModel):
    country: Optional[constr(strip_whitespace=True, min_length=1)] = None  # type: ignore
    company: Optional[constr(strip_whitespace=True, min_length=1)] = None  # type: ignore
