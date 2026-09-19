from flask import  jsonify
from app.errors.exceptions import InvalidSortFieldError

def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "error": "Product not found",
            "status": 404
        }), 404



    @app.errorhandler(InvalidSortFieldError)
    def handle_invalid_sort_field(error):
        return jsonify({
            "error": str(error),
            "status": 400
        }), 400
