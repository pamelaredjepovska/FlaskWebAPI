from flask import Blueprint, jsonify

from src.main_api import main_api_blueprint as bp


@bp.route("/health")
def health_check():
    return jsonify({"status": "Healthy"}), 200
