import json

from flask import jsonify


def swagger_config(app):
    @app.route("/swagger")
    def swagger_spec():
        try:
            json_file_path = "src/resources/swagger_config.json"

            # Open the JSON file in read mode
            with open(json_file_path, "r") as fp:
                swagger_docs = json.load(fp)
                # Return the JSON content with a 200 status code
                return jsonify(swagger_docs[0]), 200
        except FileNotFoundError:
            # Handle file not found error
            return jsonify({"error": "swagger_config.json file not found"}), 404
        except json.JSONDecodeError:
            # Handle JSON decoding error
            return (
                jsonify({"error": "Error decoding JSON from swagger_config.json"}),
                500,
            )
