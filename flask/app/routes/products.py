import math

from flask import Blueprint, jsonify, request, abort

from app.models import Product
from app.extensions import db

from app.services.product_service  import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product as delete_product_service
)

products_bp = Blueprint("products", __name__)


@products_bp.route("/api/products")
def products():
    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "id")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    min_stock = request.args.get("min_stock")
    max_stock = request.args.get("max_stock")

    if min_price is not None:
        try:
            min_price = float(min_price)
        except ValueError:
            return jsonify({
                "error": "min_price must be a number",
                "status": 400
            }), 400

    if max_price is not None:
        try:
            max_price = float(max_price)
        except ValueError:
            return jsonify({
                "error": "max_price must be a number",
                "status": 400
            }), 400

    if min_stock is not None:
        try:
            min_stock = int(min_stock)
        except ValueError:
            return jsonify({
                "error": "min_stock must be an integer",
                "status": 400
            }), 400

    if max_stock is not None:
        try:
            max_stock = int(max_stock)
        except ValueError:
            return jsonify({
                "error": "max_stock must be an integer",
                "status": 400
            }), 400

    page_arg = request.args.get("page")
    per_page_arg = request.args.get("per_page")

    if page_arg is None:
        page = 1
    else:
        try:
            page = int(page_arg)
        except ValueError:
            return jsonify({
                "error": "page must be an integer",
                "status": 400
            }), 400

    if per_page_arg is None:
        per_page = 10
    else:
        try:
            per_page = int(per_page_arg)
        except ValueError:
            return jsonify({
                "error": "per_page must be an integer",
                "status": 400
            }), 400

    if page < 1:
        return jsonify({
            "error": "page must be greater than or equal to 1",
            "status": 400
        }), 400

    if per_page < 1 or per_page > 100:
        return jsonify({
            "error": "per_page must be between 1 and 100",
            "status": 400
        }), 400

    products, total = get_products(
        search=search,
        sort=sort,
        min_price=min_price,
        max_price=max_price,
        min_stock=min_stock,
        max_stock=max_stock,
        page=page,
        per_page=per_page
    )

    if products is None:
        return jsonify({
            "error": total,
            "status": 400
        }), 400

    pages = math.ceil(total / per_page)

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


@products_bp.route("/api/products/<int:id>", methods=["GET", "PUT", "PATCH"])
def product(id):
    product = get_product(id)

    if product is None:
        abort(404)

    if request.method == "GET":
        return jsonify({
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }
        })

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON",
            "status": 400
        }), 400

    if request.method == "PUT":
        name = data.get("name")
        price = data.get("price")
        stock = data.get("stock")

        if not name:
            return jsonify({
                "error": "Product name is required",
                "status": 400
            }), 400

        if price is None:
            return jsonify({
                "error": "Product price is required",
                "status": 400
            }), 400

        if stock is None:
            return jsonify({
                "error": "Product stock is required",
                "status": 400
            }), 400

    else:
        name = data.get("name", product.name)
        price = data.get("price", product.price)
        stock = data.get("stock", product.stock)

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return jsonify({
            "error": "Product price must be a number",
            "status": 400
        }), 400

    if isinstance(stock, bool) or not isinstance(stock, int):
        return jsonify({
            "error": "Product stock must be an integer",
            "status": 400
        }), 400

    if price < 0:
        return jsonify({
            "error": "Product price cannot be negative",
            "status": 400
        }), 400

    if stock < 0:
        return jsonify({
            "error": "Product stock cannot be negative",
            "status": 400
        }), 400

    product = update_product(product, name, price, stock)

    return jsonify({
        "message": "Product updated successfully",
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        }
    })


@products_bp.route("/api/products", methods=["POST"])
def create_product_route():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON",
            "status": 400
        }), 400

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name:
        return jsonify({
            "error": "Product name is required",
            "status": 400
        }), 400

    if price is None:
        return jsonify({
            "error": "Product price is required",
            "status": 400
        }), 400

    if stock is None:
        return jsonify({
            "error": "Product stock is required",
            "status": 400
        }), 400

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return jsonify({
            "error": "Product price must be a number",
            "status": 400
        }), 400

    if isinstance(stock, bool) or not isinstance(stock, int):
        return jsonify({
            "error": "Product stock must be an integer",
            "status": 400
        }), 400

    if price < 0:
        return jsonify({
            "error": "Product price cannot be negative",
            "status": 400
        }), 400

    if stock < 0:
        return jsonify({
            "error": "Product stock cannot be negative",
            "status": 400
        }), 400

    new_product = create_product(
        name=name,
        price=price,
        stock=stock
    )


    return jsonify({
        "message": "Product created successfully",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
            "stock": new_product.stock
        }
    }), 201

@products_bp.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = get_product(id)

    if product is None:
        abort(404)

    delete_product_service(product)

    return jsonify({
        "message": "Product deleted successfully"
    })
