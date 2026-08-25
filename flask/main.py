from flask import Flask, jsonify, request
from models import db, Product

import os

app = Flask(__name__)
user = os.getenv("DB_USER")
host = os.getenv("DB_HOST")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")



app.config["SQLALCHEMY_DATABASE_URI"] = (
   f"mysql+pymysql://{user}:{password}@{host}/{database}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with  app.app_context():
    db.create_all()



@app.route("/api/hello")
def hello():

    return jsonify({
        "message": "Hello from Flask API"
    })


@app.route("/api/products")
def products():

     products = Product.query.all()

     products_list = []

     for product in products:

         product_data = {
             "id": product.id,
             "name": product.name,
             "price": product.price,
             "stock": product.stock
         }


         products_list.append(product_data)

     return jsonify(products_list)


@app.route("/api/products/<int:id>", methods=["GET", "PUT", "PATCH"])
def product(id):

    product = Product.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        })

    data = request.get_json()


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
    data = request.get_json()

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
        return  jsonify({
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
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)





