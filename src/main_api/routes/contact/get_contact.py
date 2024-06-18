import json

from flask import abort, current_app, request
from psycopg import OperationalError, ProgrammingError

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/contact")
def get_contact():
    try:
        db_pool = current_app.config["db_pool"]
        query = """SELECT json_agg(
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
                    company ON contact.company_id = company.id;
                """
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                contacts = cursor.fetchone()

        if not contacts:
            current_app.logger.debug(
                "No contact records were found at %s", request.endpoint
            )
            abort(404, description="No contact records were found.")

        return contacts

    except (OperationalError, ProgrammingError) as e:
        abort(500, description=json.loads(e.json()))  # Internal Server Error
