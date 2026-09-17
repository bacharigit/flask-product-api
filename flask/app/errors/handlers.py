from flask import  jsonify


def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "error": "Product not found",
            "status": 404
        }), 404
