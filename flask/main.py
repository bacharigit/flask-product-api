import math
from flask import Flask, jsonify, request, abort
from models import db, Product

from config import Config, get_database_uri

def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/api/hello")
    def hello():
        return jsonify({
            "message": "Hello from Flask API"
        })

    @app.route("/api/products")
    def products():

        page_arg = request.args.get("page")
        per_page_arg = request.args.get("per_page")

        if page_arg is None:
            page = 1

        else:
            try:
                page = int(page_arg)
            except  ValueError:
                return jsonify({
                    "error": "page must be an integer"
                }), 400

        if per_page_arg is None:
            per_page = 10

        else:
            try:
                per_page = int(per_page_arg)
            except ValueError:
                return jsonify({
                    "error": "per_page must be an integer"
                }), 400

        if page < 1:
            return jsonify({
                "error": "page must be greater than or equal to 1"
            }), 400

        if per_page < 1 or per_page > 100:
            return jsonify({
                "error": "per_page must be between 1 and 100"
            }), 400

        offset = (page -1) * per_page

        total = Product.query.count()
        pages = math.ceil(total / per_page)


        products = (
            Product.query
            .order_by(Product.id)
            .limit(per_page)
            .offset(offset)
            .all()
        )

        products_list = []

        for product in products:
            product_data = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }

            products_list.append(product_data)

        return jsonify({
            "products": products_list,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": pages
            }

        })

    @app.route("/api/products/<int:id>", methods=["GET", "PUT", "PATCH"])
    def product(id):
        product = get_product_or_404(id)

        if request.method == "GET":
            return jsonify({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            })

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Request body must contain JSON"
            }), 400

        if request.method == "PUT":
            name = data.get("name")
            price = data.get("price")
            stock = data.get("stock")

            if not name:
                return jsonify({
                    "error": "Product name is required"
                }), 400

            if price is None:
                return jsonify({
                    "error": "Product price is required"
                }), 400

            if stock is None:
                return jsonify({
                    "error": "Product stock is required"
                }), 400

        else:
            name = data.get("name", product.name)
            price = data.get("price", product.price)
            stock = data.get("stock", product.stock)

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            return jsonify({
                "error": "Product price must be a number"
            }), 400

        if isinstance(stock, bool) or not isinstance(stock, int):
            return jsonify({
                "error": "Product stock must be an integer"
            }), 400

        if price < 0:
            return jsonify({
                "error": "Product price cannot be negative"
            }), 400

        if stock < 0:
            return jsonify({
                "error": "Product stock cannot be negative"
            }), 400

        product.name = name
        product.price = price
        product.stock = stock

        db.session.commit()

        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }
        })

    @app.route("/api/products", methods=["POST"])
    def create_product():
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Request body must contain JSON"
            }), 400

        name = data.get("name")
        price = data.get("price")
        stock = data.get("stock")

        if not name:
            return jsonify({
                "error": "Product name is required"
            }), 400

        if price is None:
            return jsonify({
                "error": "Product price is required"
            }), 400

        if stock is None:
            return jsonify({
                "error": "Product stock is required"
            }), 400

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            return jsonify({
                "error": "Product price must be a number"
            }), 400

        if isinstance(stock, bool) or not isinstance(stock, int):
            return jsonify({
                "error": "Product stock must be an integer"
            }), 400

        if price < 0:
            return jsonify({
                "error": "Product price cannot be negative"
            }), 400

        if stock < 0:
            return jsonify({
                "error": "Product stock cannot be negative"
            }), 400

        new_product = Product(
            name=name,
            price=price,
            stock=stock
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product": {
                "id": new_product.id,
                "name": new_product.name,
                "price": new_product.price,
                "stock": new_product.stock
            }
        }), 201

    @app.route("/api/products/<int:id>", methods=["DELETE"])
    def delete_product(id):
        product = get_product_or_404(id)

        db.session.delete(product)
        db.session.commit()

        return jsonify({
            "message": "Product deleted successfully"
        })

    return app


def get_product_or_404(id):
    product = db.session.get(Product, id)

    if product is None:
        abort(404)

    return product


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

