

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



def test_get_products_invalid_page_type(client):

    response = client.get("/api/products?page=abc")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "page must be an integer"



def test_get_products_invalid_per_page_type(client):

    response = client.get("/api/products?per_page=abc")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "per_page must be an integer"



def test_get_product(client, product):

    response = client.get(f"/api/products/{product.id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == product.id
    assert data["name"] == "Test Product"
    assert data["price"] == 100
    assert data["stock"] == 10


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


def test_create_product_missing_json(client):
    response = client.post(
        "/api/products"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Request body must contain JSON" 



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
