from flask import Blueprint, jsonify

general_bp = Blueprint("general", __name__)


@general_bp.route("/api/hello")
def hello():
    return jsonify({
        "message": "Hello from Flask API"
    })
