from flask import Blueprint, jsonify

main_api = Blueprint("main_api", __name__)


@main_api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Healthy"}), 200
