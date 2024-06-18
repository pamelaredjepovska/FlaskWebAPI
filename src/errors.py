from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP errors
        if isinstance(e, HTTPException):
            response = e.get_response()
            response.data = jsonify(
                {
                    "code": e.code,
                    "name": e.name,
                    "description": e.description,
                }
            ).data
            response.content_type = "application/json"
            return response
        # Now you're handling non-HTTP exceptions only
        return (
            jsonify(
                {
                    "code": 500,
                    "name": "Internal Server Error",
                    "description": "An unexpected error has occurred.",
                }
            ),
            500,
        )
