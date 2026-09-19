from app.extensions import db
from app.models  import  Product

def test_hello(client):

    response = client.get("/api/hello")

    assert response.status_code == 200

    assert response.get_json() == {
        "message": "Hello from Flask API"
    }


def test_get_products(client):

     response = client.get("/api/products")

     assert response.status_code == 200

     data = response.get_json()

     assert isinstance(data, dict)
     assert "products" in data
     assert "pagination" in data


def test_get_products_pagination(client, products):
    response = client.get("/api/products?page=1&per_page=2")

    assert response.status_code == 200

    data =  response.get_json()

    assert len(data["products"]) == 2

    assert data["products"][0]["name"] == "Product 1"
    assert data["products"][1]["name"] == "Product 2"


    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total"] == 4
    assert data["pagination"]["pages"] == 2



def test_get_products_pagination_page_2(client, products):

    response = client.get("/api/products?page=2&per_page=2")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["products"]) == 2

    assert data["products"][0]["name"] == "Product 3"
    assert data["products"][1]["name"] == "Product 4"

    assert data["pagination"]["page"] == 2
    assert data["pagination"]["per_page"] == 2



def test_get_products_pagination_page_beyond_last(client, products):

    response = client.get("/api/products?page=3&per_page=2")

    assert response.status_code == 200

    data = response.get_json()

    assert data["products"] == []

    assert data["pagination"]["page"] == 3
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total"] == 4
    assert data["pagination"]["pages"] == 2



def test_get_products_invalid_page(client):

    response = client.get("/api/products?page=0")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "page must be greater than or equal to 1"

    assert data["status"] == 400


def test_get_products_invalid_per_page(client):

     response = client.get("/api/products?per_page=101")

     assert response.status_code == 400

     data = response.get_json()

     assert data["error"] == "per_page must be between 1 and 100"



def test_get_products_invalid_per_page_zero(client):

    response = client.get("/api/products?per_page=0")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "per_page must be between 1 and 100"

    assert data["status"] == 400



def test_get_products_invalid_page_type(client):

    response = client.get("/api/products?page=abc")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "page must be an integer"

    assert data["status"] == 400



def test_get_products_invalid_per_page_type(client):

    response = client.get("/api/products?per_page=abc")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "per_page must be an integer"

    assert data["status"] == 400


def test_get_product(client, product):

    response = client.get(f"/api/products/{product.id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["product"]["id"] == product.id
    assert data["product"]["name"] == product.name
    assert data["product"]["price"] == product.price
    assert data["product"]["stock"] == product.stock


def test_create_product(client):

     response = client.post(
         "/api/products",
         json={
             "name": "Keyboard",
             "price": 100,
             "stock": 10
         }
     )

     assert response.status_code == 201

     data = response.get_json()

     assert data["message"] == "Product created successfully"

     assert data["product"]["name"] == "Keyboard"
     assert data["product"]["price"] == 100
     assert data["product"]["stock"] == 10


def test_update_product_put(client, product):

     response = client.put(
         f"/api/products/{product.id}",
         json={
             "name": "Updated Keyboard",
             "price": 200,
             "stock": 25
         }
     )

     assert response.status_code == 200

     data = response.get_json()

     assert data["message"] == "Product updated successfully"

     assert data["product"]["name"] == "Updated Keyboard"
     assert data["product"]["price"] == 200
     assert data["product"]["stock"] == 25


def test_update_product_put_nonexistent(client):

    response = client.put("/api/products/99999",
        json={
            "name": "Keyboard",
            "price": 100,
            "stock": 10
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Product not found"
    assert data["status"] == 404


def test_update_product_patch_nonexistent(client):

    response = client.put("/api/products/99999",
        json={
            "price": 100,
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Product not found"
    assert data["status"] == 404


def test_update_product_patch(client, product):

    response = client.patch(
        f"/api/products/{product.id}",
        json={
            "price": 250
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Product updated successfully"

    assert data["product"]["name"] == "Test Product"
    assert data["product"]["price"] == 250
    assert data["product"]["stock"] == 10


def test_delete_product(client, product):

    response = client.delete(f"/api/products/{product.id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Product deleted successfully"

    response = client.get(f"/api/products/{product.id}")

    assert response.status_code == 404


def test_get_nonexistent_product(client):
    response = client.get("/api/products/999999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Product not found"
    assert data["status"] == 404


def test_create_product_missing_json(client):
    response = client.post(
        "/api/products"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Request body must contain JSON" 
    assert data["status"] == 400


def test_create_product_missing_name(client):
    response = client.post(
        "/api/products",
        json={
            "price": 100,
            "stock": 10
        }
    )


    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product name is required"
    assert data["status"] == 400

def test_create_product_missing_price(client):
    response = client.post(
       "/api/products",
       json={
           "name": "Keyboard",
           "stock": 10
       }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product price is required"
    assert data["status"] == 400


def test_create_product_missing_stock(client):
    response = client.post(
       "/api/products",
       json={
           "name": "Keyboard",
           "price": 100
       }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock is required"
    assert data["status"] == 400

def test_create_product_negative_price(client):
    response  = client.post(
        "/api/products",
        json={
            "name": "Keyboard",
            "price": -100,
            "stock": 10
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product price cannot be negative"
    assert data["status"] == 400

def test_create_product_negative_stock(client):
    response = client.post(
        "/api/products",
        json={
            "name": "Keyboard",
            "price": 100,
            "stock": -10
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock cannot be negative"
    assert data["status"] == 400

def test_create_product_invalid_price_type(client):
    response = client.post(
        "/api/products",
        json={
            "name": "Keyboard",
            "price": "100",
            "stock": 10
        }
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Product price must be a number"
    assert data["status"] == 400


def test_create_product_invalid_stock_type(client):
    response = client.post(
        "/api/products",
        json={
            "name": "Keyboard",
            "price": 100,
            "stock": "10"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock must be an integer"
    assert data["status"] == 400

def test_update_product_put_missing_json(client, product):
    response = client.put(
        f"/api/products/{product.id}",
    )

    assert response.status_code == 400

    data = response.get_json()
    assert data["error"] == "Request body must contain JSON"


def test_update_product_put_missing_name(client, product):
    response = client.put(
        f"/api/products/{product.id}",
        json={
            "price": 200,
            "stock": 25
        }
    )

    assert response.status_code == 400

    data = response.get_json()


    assert data["error"] == "Product name is required"


def test_update_product_put_missing_price(client, product):
    response = client.put(
        f"/api/products/{product.id}",
        json={
            "name": "Updated Keyboard",
            "stock": 25
        }
    )
    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product price is required"



def test_update_product_put_missing_stock(client, product):
    response = client.put(
        f"/api/products/{product.id}",
        json={
            "name": "Updated Keyboard",
            "price": 200
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock is required"


def test_update_product_put_negative_price(client, product):
    response = client.put(
        f"/api/products/{product.id}",
        json={
            "name": "Updated Keyboard",
            "price": -100,
            "stock": 25
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product price cannot be negative"


def test_update_product_put_negative_stock(client, product):
    response = client.put(
        f"/api/products/{product.id}",
        json={
            "name": "Updated Keyboard",
            "price": 100,
            "stock": -25
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock cannot be negative"



def test_update_product_put_invalid_price_type(client, product):
    response = client.put(
        f"/api/products/{product.id}",
        json={
            "name": "Updated Keyboard",
            "price": "200",
            "stock": 25
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product price must be a number"


def test_update_product_put_invalid_stock_type(client, product):
    response = client.put(
        f"/api/products/{product.id}",
        json={
            "name": "Updated Keyboard",
            "price": 200,
            "stock": "25"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock must be an integer"


def test_update_product_patch_missing_json(client, product):
    response = client.patch(
        f"/api/products/{product.id}"

    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Request body must contain JSON"


def test_update_product_patch_negative_price(client, product):
    response = client.patch(
        f"/api/products/{product.id}",
        json={
            "price": -100
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product price cannot be negative"

def test_update_product_patch_negative_stock(client, product):
    response = client.patch(
        f"/api/products/{product.id}",
        json={
            "stock": -25
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock cannot be negative"


def test_update_product_patch_invalid_price_type(client, product):
    response = client.patch(
        f"/api/products/{product.id}",
        json={
            "price": "250"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product price must be a number"


def test_update_product_patch_invalid_stock_type(client, product):
    response = client.patch(
        f"/api/products/{product.id}",
        json={
            "stock": "10"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Product stock must be an integer"


def test_products_are_clean_after_create(client):
    response = client.get("/api/products")

    assert response.status_code == 200

    data = response.get_json()

    for product in data["products"]:
        assert product["name"] != "Keyboard"

def test_search_products(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Wireless Keyboard", price=150, stock=20),
            Product(name="Mouse", price=50, stock=30),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["products"]) == 2
    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Wireless Keyboard"


def test_search_products_lowercase(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Wireless Keyboard", price=150, stock=20),
            Product(name="Mouse", price=50, stock=30),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=keyboard")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["products"]) == 2
    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Wireless Keyboard"


def test_search_products_no_results(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Mouse", price=50, stock=30),
        ]


        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Monitor")

    assert response.status_code == 200

    data = response.get_json()

    assert data["products"] == []
    assert data["pagination"]["total"] == 0
    assert data["pagination"]["pages"] == 0



def test_search_products_empty_search(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Mouse", price=50, stock=30),
        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?search=")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["products"]) == 2
    assert data["pagination"]["total"] == 2



def test_search_products_pagination(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Wireless Keyboard", price=150, stock=8),
            Product(name="Gaming Keyboard", price=200, stock=12),
            Product(name="Mouse", price=180, stock=10),
            Product(name="Monitor", price=800, stock=17),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard&page=1&per_page=2")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["products"]) == 2
    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Wireless Keyboard"

    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total"] == 3
    assert data["pagination"]["pages"] == 2



def test_search_products_pagination_page2(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Wireless Keyboard", price=150, stock=8),
            Product(name="Gaming Keyboard", price=200, stock=12),
            Product(name="Mouse", price=180, stock=10),
            Product(name="Monitor", price=800, stock=17),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard&page=2&per_page=2")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["products"]) == 1
    assert data["products"][0]["name"] == "Gaming Keyboard"

    assert data["pagination"]["page"] == 2
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total"] == 3
    assert data["pagination"]["pages"] == 2




def test_search_products_pagination_page_beyond_last(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Wireless Keyboard", price=150, stock=8),
            Product(name="Gaming Keyboard", price=200, stock=12),
            Product(name="Mouse", price=180, stock=10),
            Product(name="Monitor", price=800, stock=17),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard&page=3&per_page=2")

    assert response.status_code == 200

    data = response.get_json()

    assert data["products"] == []

    assert data["pagination"]["page"] == 3
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total"] == 3
    assert data["pagination"]["pages"] == 2


def test_get_products_sort_by_price(client, app):

    with app.app_context():
        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()



    response = client.get("/api/products?sort=price")

    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Mouse"
    assert data["products"][1]["name"] == "Webcame"
    assert data["products"][2]["name"] == "Keyboard"
    assert data["products"][3]["name"] == "Monitor"



def test_get_products_sort_by_price_descending(client, app):

    with app.app_context():
        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()



    response = client.get("/api/products?sort=-price")

    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Monitor"
    assert data["products"][1]["name"] == "Keyboard"
    assert data["products"][2]["name"] == "Webcame"
    assert data["products"][3]["name"] == "Mouse"


def test_get_products_sort_by_name(client, app):

    with app.app_context():
        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?sort=name")

    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Monitor"
    assert data["products"][2]["name"] == "Mouse"
    assert data["products"][3]["name"] == "Webcame"


def test_get_products_sort_by_name_descending(client, app):

    with app.app_context():
        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?sort=name")

    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Monitor"
    assert data["products"][2]["name"] == "Mouse"
    assert data["products"][3]["name"] == "Webcame"


def test_get_products_invalid_sort_field(client):
    response = client.get("/api/products?sort=banana")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid sort field"

    assert data["status"] == 400

def test_get_products_min_price(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),

        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?min_price=300")
  
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Monitor"
    assert data["pagination"]["total"] == 2
   


def test_get_products_max_price(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),

        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?max_price=300")
  
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Mouse"
    assert data["products"][2]["name"] == "Webcame"
    assert data["pagination"]["total"] == 3


def test_get_products_price_range(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),

        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?min_price=200&max_price=300")
  
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Webcame"
    assert data["pagination"]["total"] == 2

def test_get_products_min_stock(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?min_stock=30")
  
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Mouse"
    assert data["products"][1]["name"] == "Webcame"
    assert data["pagination"]["total"] == 2
   


def test_get_products_max_stock(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),

            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?max_stock=30")
 
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Mouse"
    assert data["products"][2]["name"] == "Monitor"
    assert data["pagination"]["total"] == 3


 
def test_get_products_stock_range(client, app):
    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=300, stock=10),
            Product(name="Mouse", price=100, stock=30),
            Product(name="Monitor", price=500, stock=20),
            Product(name="Webcame", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()


    response = client.get("/api/products?min_stock=10&max_stock=30")
 
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["products"][1]["name"] == "Mouse"
    assert data["products"][2]["name"] == "Monitor"
    assert data["pagination"]["total"] == 3


def test_get_product_invalid_min_price(client):

    response = client.get("/api/products?min_price=abc")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "min_price must be a number"
    assert data["status"] == 400


def test_get_product_invalid_max_price(client):

    response = client.get("/api/products?max_price=abc")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "max_price must be a number"
    assert data["status"] == 400


def test_get_products_invalid_min_stock(client):
    response = client.get("/api/products?min_stock=abc")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "min_stock must be an integer"

    assert data["status"] == 400


def test_get_products_invalid_max_stock(client):
    response = client.get("/api/products?max_stock=abc")
    
    assert response.status_code == 400

    data = response.get_json()
    
    assert data["error"] == "max_stock must be an integer"

    assert data["status"] == 400


def test_get_products_search_with_price_range(client, app):

    with app.app_context():
        Product.query.delete()

        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Gaming Keyboard", price=500, stock=30),
            Product(name="Mouse", price=500, stock=20),
            Product(name="Wifi Keyboard", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard&min_price=200&max_price=500")
    
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Gaming Keyboard"
    assert data["products"][1]["name"] == "Wifi Keyboard"
    assert data["pagination"]["total"] == 2


def test_get_products_search_with_stock_range(client, app):

    with app.app_context():
        Product.query.delete()


        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Gaming Keyboard", price=500, stock=30),
            Product(name="Mouse", price=500, stock=20),
            Product(name="Wifi Keyboard", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard&min_stock=10&max_stock=20")
    
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Keyboard"
    assert data["pagination"]["total"] == 1



def test_get_products_search_stock_range_sorted(client, app):

    with app.app_context():
        Product.query.delete()


        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Gaming Keyboard", price=500, stock=30),
            Product(name="Mouse", price=500, stock=20),
            Product(name="Wifi Keyboard", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard&min_stock=10&max_stock=30&sort=-stock")
    
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Gaming Keyboard"
    assert data["products"][1]["name"] == "Keyboard"
    assert data["pagination"]["total"] == 2



def test_get_products_search_stock_range_sorted_paginated(client, app):

    with app.app_context():
        Product.query.delete()


        products = [
            Product(name="Keyboard", price=100, stock=10),
            Product(name="Gaming Keyboard", price=500, stock=30),
            Product(name="Mouse", price=500, stock=20),
            Product(name="Wifi Keyboard", price=200, stock=40),
        ]

        db.session.add_all(products)
        db.session.commit()

    response = client.get("/api/products?search=Keyboard&min_stock=10&max_stock=40&sort=-stock&page=1&per_page=2")
    
    assert response.status_code == 200

    data = response.get_json()

    assert data["products"][0]["name"] == "Wifi Keyboard"
    assert data["products"][1]["name"] == "Gaming Keyboard"

    assert data["pagination"]["page"] == 1
    assert data["pagination"]["pages"] == 2
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total"] == 3


