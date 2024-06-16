from flask import jsonify


def swagger_config(app):
    @app.route("/swagger")
    def swagger_spec():
        return jsonify(
            {
                "swagger": "2.0",
                "info": {
                    "title": "My Flask API",
                    "description": "API documentation with Swagger UI",
                    "version": "1.0.0",
                },
                "host": "localhost:5000",
                "basePath": "/main_api",
                "schemes": ["http"],
                "paths": {
                    "/health": {
                        "get": {
                            "summary": "Health Check",
                            "description": "Check the health status of the API",
                            "responses": {
                                "200": {
                                    "description": "API is healthy",
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {
                                                "type": "string",
                                                "example": "Healthy",
                                            }
                                        },
                                    },
                                }
                            },
                        }
                    },
                },
            }
        )
