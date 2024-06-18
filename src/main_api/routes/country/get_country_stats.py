import json
from typing import Optional

from flask import abort, current_app, request
from psycopg import OperationalError, ProgrammingError, sql
from pydantic import BaseModel, ValidationError, constr

from src import get_db_connection
from src.main_api import main_api_blueprint as bp


@bp.route("/country/stats")
def get_country_stats():
    try:
        # Validate the request arguments
        try:
            args = CountryStatsParams(**request.args.to_dict())
        except ValidationError as e:
            current_app.logger.debug(
                "%s : Validation error in %s", str(e), request.endpoint
            )
            abort(400, description=json.loads(e.json()))

        # Generate the stats query
        stats_query = sql.SQL(
            """SELECT
                    c.name AS company,
                    COUNT(ct.id) AS num_of_contacts
                FROM
                    company c
                JOIN
                    contact ct ON c.id = ct.company_id
                JOIN
                    country cn ON ct.country_id = cn.id
                WHERE
                    cn.name = %(country)s
                GROUP BY
                    c.id
                ORDER BY
                    c.name;"""
        )

        db_pool = current_app.config["db_pool"]
        with get_db_connection(db_pool) as conn:
            with conn.cursor() as cursor:
                stats_query_params = {"country": args.country}
                cursor.execute(stats_query, stats_query_params)
                stats_result = cursor.fetchall()

                # If there are no records with the requested filter(s), abort
                if not stats_result:
                    current_app.logger.debug(
                        "No statistics records were found at %s", request.endpoint
                    )
                    abort(
                        404,
                        description="No statistics records were found for the requested country.",
                    )

        return stats_result
    except (OperationalError, ProgrammingError) as e:
        current_app.logger.error("Server error: %s, %s", request.endpoint, str(e))
        return abort(500, description=json.loads(e.json()))  # Internal Server Error


class CountryStatsParams(BaseModel):
    country: Optional[constr(strip_whitespace=True, min_length=1)]  # type: ignore
