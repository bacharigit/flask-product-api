# Flask Product REST API

> **Version:** v1.0.0
> **Current development:** Testing and architecture refactorung

A Flask REST API for managing products using **Flask**, **MySQL**, **SQLAlchemy**, **Docker**, and **Docker Compose**, and **pytest**.

This project provides product CRUD operations through a REST API using JSON .It  is also being developed  with an emphasis on understanding Flask application structure, database communication, testing, fixtures, configuration.

## Features

### API

* Product CRUD operations
* JSON responses
* GET products
* POST products
* PUT products
* PATCH products
* DELETE products
* Input validation
* Error handling
* HTTP 404 handling
* pagination
* Configurable page size

### Database

* MySQL 8.0
* SQLAlchemy ORM
* Persistent MySQL data using Docker volumes

### Testing

* pytest
* Flask test client
* Application Factory pattern
* Dedicated test configuration
* Dedicated test database
* pytest fixtures
* Automatic test cleanup
* Product test fixtures
* API endpoint testing
* Pagination testing
* Validation testing

### Docker

* Dockerized Flask application
* Docker Compose
* Flask and MySQL containers
* MySQL health check
* Environment variable configuration
* Persistent MySQL volume

---

## API Endpoints

| Method | Endpoint             | Description                |
| ------ | -------------------- | -------------------------- |
| GET    | `/api/hello`         | Test the API               |
| GET    | `/api/products`      | Get all products           |
| POST   | `/api/products`      | Create a product           |
| GET    | `/api/products/<id>` | Get one product            |
| PUT    | `/api/products/<id>` | Replace a product          |
| PATCH  | `/api/products/<id>` | Partially update a product |
| DELETE | `/api/products/<id>` | Delete a product           |

---

## Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* MySQL
* PyMySQL
* pytest
* Docker
* Docker Compose


---

## Pagination

The `GET /api/products` endpoint supports pagination using the `page` and `per_page` query parameters.

Example:

```text
/api/products?page=2&per_page=10
```

Where:

* `page` specifies the page number.
* `per_page` specifies how many products are returned per page.

The API validates both parameters.

For example:

```text
/api/products?page=0
```

returns:

```json
{
  "error": "page must be greater than or equal to 1"
}
```

An invalid `per_page` value also returns a `400 Bad Request`.

Example:

```text
/api/products?per_page=101
```
returns:

```json
{
  "error": "per_page must be between 1 and 100"
}
```

The response includes pagination metadata:

```json
{
  "products": [
    {
      "id": 1,
      "name": "Keyboard",
      "price": 100,
      "stock": 10
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 1,
    "pages": 1
  }
}
```

Pagination is implemented using SQLAlchemy `limit()` and `offset()`.

## Project Structure

```text
.
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
│
├── flask
│   ├── config.py
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   │
│   └── tests
│       ├── conftest.py
│       ├── __init__.py
│       └── test_products.py
│
└── mysql
    └── init
```

> The `.env` file is intentionally not included in the repository because it contains sensitive configuration.

---

# Application Architecture

The application uses the **Application Factory pattern**.

Instead of creating the Flask application immediately when `main.py` is imported, the project defines:

```python
create_app()
```

The application is created when the factory is called.

This provides a cleaner separation between:

* application creation
* configuration
* database initialization
* testing
* normal application execution

The structure allows pytest to create a separate Flask application using `TestingConfig`.

---


## Normal Application Execution

When the application is started with Docker Compose:

```bash
sudo docker compose up --build
```

the general flow is:

```text
Docker Compose
      │
      ▼
Flask Container
      │
      ▼
main.py
      │
      ├── models.py
      │
      └── config.py
      │
      ▼
create_app()
      │
      ├── Load configuration
      ├── Configure database URI
      ├── Initialize SQLAlchemy
      ├── Create database tables
      └── Register routes
      │
      ▼
Flask Development Server
      │
      ▼
HTTP Requests
      │
      ▼
SQLAlchemy
      │
      ▼
MySQL
```

---

# Testing Architecture

Tests are located in:

```text
flask/tests/
```

pytest uses fixtures defined in:

```text
flask/tests/conftest.py
```

The test application is created using:

```python
create_app(TestingConfig)
```

This means the tests use a separate database:

```text
store_test
```

rather than the normal application database.

This prevents test data from being mixed with development data.

---
## Test Fixtures

The project currently uses several pytest fixtures.

### `app`

Creates the Flask application using `TestingConfig`.

```python
@pytest.fixture
def app():
    return create_app(TestingConfig)
```

### `client`

Creates Flask's test client.

```python
@pytest.fixture
def client(app):
    return app.test_client()
```

This allows tests to make HTTP requests without starting a real web server.

For example:

```python
response = client.get("/api/products")
```
### `product`

Creates a known test product for tests that need an existing product.

```python
@pytest.fixture
def product(app):
    ...
```

### `clean_products`

Automatically removes test products after each test.

The test database is dedicated to automated testing, so clearing the product table after each test keeps tests isolated.

---

# Running the Application

## Prerequisites

Install:

* Docker
* Docker Compose

---

## Environment Configuration

Create the `.env` file from the example:

```bash
cp .env.example .env
```
Then configure the required values.

Example: 

```env
DB_PASSWORD=your-database-password
DB_NAME=store
TEST_DB_NAME=store_test
```
## Build and start

Start the application:

```bash
sudo docker compose up --build
```

The API will be available at:

```text
http://localhost:5000
```

Test the API:

```text
http://localhost:5000/api/hello
```

---

## Stop the Application

Press:

```text
Ctrl+C
```

or run:

```bash
sudo docker compose down
```
# MySQL

The application uses MySQL 8.0.

The MySQL service is defined in:

```text
docker-compose.yml
```

The database uses a named Docker volume:

```yaml
volumes:
  - mysql-data:/var/lib/mysql
```

This allows database data to persist when containers are stopped or recreated.

MySQL also has a health check so that the Flask service can wait for MySQL to become ready.

---
# Testing

Tests can be executed inside a temporary Flask container.

Run:

```bash
sudo docker compose run --rm flask pytest
```

The `--rm` option removes the temporary test container after pytest finishes.

The tests use the dedicated:

```text
store_test
```

database.

After the tests complete, the test product data is cleaned up.

---

## Test Coverage

The test suite covers areas including:

* `/api/hello`
* Getting products
* Creating products
* Getting individual products
* Updating products with PUT
* Updating products with PATCH
* Deleting products
* Missing product handling
* Missing JSON bodies
* Missing product names
* Missing prices
* Missing stock values
* Invalid price types
* Invalid stock types
* Negative prices
* Negative stock
* Boolean validation
* Response status codes
* JSON response data
* Invalid pagination parameters
* Pagination page boundaries
* Pagination metadata

---

### Validation testing

The API validates product data and returns HTTP `400 Bad Request` for invalid input.

Examples of invalid data include:

* Missing product name
* Missing price
* Missing stock
* Negative price
* Negative stock
* Non-numeric price
* Non-integer stock
* Boolean values used as price or stock
* Missing JSON request body

Pagination parameters are also validated.
A nonexistent product returns HTTP `404 Not Found`.

---

## Docker Hub

The Docker image is available on Docker Hub:

`bacharidocker/flask-product-api`

### Pull the released image

```bash
docker pull bacharidocker/flask-product-api:v1.0.0
```

The `latest` tag is also available:

```bash
docker pull bacharidocker/flask-product-api:latest
```

The Docker image contains the Flask REST API application.

Docker Compose is recommended for running the complete application because the API requires the MySQL database.

---

## Version History

### v1.0.0 - Initial REST API

Completed:

* Flask REST API
* Product CRUD operations
* GET, POST, PUT, PATCH, and DELETE endpoints
* MySQL 
* SQLAlchemy ORM
* JSON responses
* Input validation
* Error handling
* Docker Compose 
* MySQL health check
* Environment variable configuration


### Testing Phase

Completed:

* pytest
* Flask test client
* API endpoint tests
* Validation tests
* Dedicated test database
* pytest fixtures
* Automatic test cleanup

---

### v1.1.0 — API Features
Completed:

* Application Factory pattern
* `TestingConfig`
* Dedicated test database configuration
* Improved fixture architecture
* Pagination
* Pagination validation
* Pagination metadata
* SQLAlchemy `limit()` and `offset()`
* Improved API response structure
* Expanded automated test coverage
* 38 passing tests

### Future Features

Planned:

* Search
* Filtering
* Sorting
* Better API error responses


### v1.2.0 — Product Images

Planned:

* Product image uploads
* Image validation
* Image replacement
* Image cleanup
* Persistent image storage

### Production

Planned:

* Gunicorn
* Nginx
* Production Docker image
* Database migrations
* CI/CD with GitHub Actions

### Advanced

Planned:

* User authentication
* Authorization
* Swagger/OpenAPI documentation
* Improved architecture
* Deployment

---
# Docker Image

The application image is available on Docker Hub:

https://hub.docker.com/r/bacharidocker/flask-product-api
---

## Author

**Hossein Bachari**

GitHub: https://github.com/bacharigit
