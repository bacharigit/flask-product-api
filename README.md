# Flask Product REST API

> **Version:** v1.2.0
> **Current development:** architecture refactoring

A Flask REST API for managing products using **Flask**, **MySQL**, **SQLAlchemy**, **Docker**,  **Docker Compose**, and **pytest**.

This project provides product CRUD operations through a REST API using JSON. It  is also being developed  with an emphasis on understanding Flask application structure, database communication, testing, fixtures, configuration.

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
* Search
* Sorting
* Filtering
* Combined query parameters
* Configurable page size
* Pagination metadata
* Application factory pattern
* Flask Blueprints for route organization
*  Dedicated error-handling module
*  Separated application entry point
* Service Layer
* Repository Layer

### Database

* MySQL 8.0
* SQLAlchemy ORM
* Persistent MySQL data using Docker volumes
* Separate test database

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
* Error response testing
* **66 passing tests**

### Docker

* Dockerized Flask application
* Docker Compose
* Flask and MySQL containers
* MySQL health check
* Environment variable configuration
* Persistent MySQL volume
* Docker Hub image
---


## Application Architecture

The application follows a layered architecture that separates HTTP handling, application logic, database access, and error handling.

### Application Factory

The application uses the Flask Application Factory pattern.

The `create_app()` function is responsible for:

* Creating the Flask application
* Loading configuration
* Initializing SQLAlchemy
* Registering Blueprints
* Registering error handlers
* Creating database tables

The application entry point is kept separate from application creation.

### Routes / Blueprints

Routes are responsible for HTTP-related concerns.


* Receive HTTP requests
* Read query parameters
* Read JSON request data
* Perform HTTP-level validation
* Call the appropriate service
* Build JSON responses
* Return HTTP status codes

Routes do not contain database queries.

For example:

```text
HTTP Request
     ↓
Product Route
     ↓
Product Service
```

### Service Layer

The Service Layer sits between the routes and the repository.

It is responsible for application and business logic and provides an abstraction between HTTP handling and database access.

For example:
```text
Route
  ↓
product_service.get_products()
  ↓
product_repository.get_products()
```

The current service layer is intentionally lightweight because the application's business logic is still relatively simple. As the application grows, more complex business rules can be handled here.

### Repository Layer

The Repository Layer is responsible for database access.

It contains SQLAlchemy queries and database operations such as:

* Retrieving products
* Searching products
* Filtering products
* Sorting products
* Paginating products
* Creating products
* Updating products
* Deleting products

For example:

```text
Service
   ↓
Repository
   ↓
SQLAlchemy
   ↓
MySQL
```

This keeps database-specific operations outside the routes and separates data access from application logic.

### Models

Models define the database structure using SQLAlchemy.

The `Product` model represents the `product` database table and defines fields such as:

* `id`
* `name`
* `price`
* `stock`

The repository uses the model when building database queries.

### Extensions

Flask extensions are defined separately in:

```text
app/extensions.py
```

The SQLAlchemy extension object is created there:

```python
db = SQLAlchemy()
```

The application factory initializes the extension with:

```python
db.init_app(app)
```

This keeps extension setup separate from the rest of the application.

### Error Handling

Error handling is implemented as a cross-cutting concern rather than as another sequential layer.

Custom exceptions are defined in:

```text
app/errors/exceptions.py
```

and centralized error handlers are registered in:

```text
app/errors/handlers.py
```

For example, an invalid sort field raises:

```python
raise InvalidSortFieldError("Invalid sort field")
```

Flask then uses the registered error handler to return a standardized HTTP response.

Errors can occur at different points in the request flow:

```text
Route ────────┐
Service ──────┼──→ Error Handling
Repository ───┘
```
### Architecture Summary
Routes       → HTTP
Services     → Business/Application Logic
Repositories → Database Access
Models       → Database Structure

Routes
  ↓
Service Layer
  ↓
Repository Layer
  ↓
SQLAlchemy / Models
  ↓
MySQL

Supporting components:

Extensions → Flask / SQLAlchemy setup
Errors     → Centralized exception handling

This architecture makes the application easier to test, maintain, and extend as new features are added.

### Request Flow

A typical product request follows this flow:

```text
Client
  │
  │ HTTP Request
  ▼
Routes / Blueprints
  │
  ▼
Service Layer
  │
  ▼
Repository Layer
  │
  │ SQLAlchemy queries
  ▼
Models / SQLAlchemy
  │
  ▼
MySQL
  │
  │ database result
  ▼
Repository
  │
  ▼
Service
  │
  ▼
Route
  │
  │ JSON Response
  ▼
Client
```

The main responsibilities are therefore:

```text
Routes       → HTTP handling
Services     → Application / business logic
Repositories → Database access
Models       → Database structure
Extensions   → Flask extension setup
Errors       → Centralized error handling
```

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

# API Querying

The `GET /api/products` endpoint supports several query parameters.


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
  "error": "page must be greater than or equal to 1",
  "status": 400
}
```

`per_page` must be between `1` and `100`.

Example:

```text
/api/products?per_page=101
```
returns:

```json
{
  "error": "per_page must be between 1 and 100",
  "status": 400
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


## Search

Products can be searched by name using the `search` query parameter.

Example:

```text
/api/products?search=keyboard
```

The API searches product names using a partial match.

Search can also be combined with pagination:

```text
/api/products?search=keyboard&page=1&per_page=10
```

---

## Sorting

Products can be sorted using the `sort` query parameter.

Supported fields are:

* `id`
* `name`
* `price`
* `stock`

Examples:

```text
/api/products?sort=price
```

Sort by price in ascending order.


```text
/api/products?sort=-price
```

Sort by price in descending order.

The `-` prefix indicates descending order.

An invalid sort field returns:

```json
{
  "error": "Invalid sort field",
  "status": 400
}
```

---

## Filtering

Products can be filtered using price and stock ranges.

### Price filtering

```text
/api/products?min_price=100
```

```text
/api/products?max_price=500
```

Both can be used together:

```text
/api/products?min_price=100&max_price=500
```

### Stock filtering

```text
/api/products?min_stock=10
```

```text
/api/products?max_stock=50
```

Both can also be combined:

```text
/api/products?min_stock=10&max_stock=50
```

Invalid filter values return HTTP `400 Bad Request`.

---

## Combining Query Parameters

Search, filtering, sorting, and pagination can be combined.

Example:

```text
/api/products?search=keyboard&min_price=50&max_price=500&min_stock=5&sort=-price&page=1&per_page=10
```

The query is built progressively:

```text
Product.query
     ↓
Search
     ↓
Price filtering
     ↓
Stock filtering
     ↓
Sorting
     ↓
Count
     ↓
Pagination
     ↓
Results
```

This allows the API to perform multiple query operations in a single request.

---

# API Response Structure

The API uses a consistent JSON structure for successful responses and errors.

## Get One Product

```json
{
  "product": {
    "id": 1,
    "name": "Keyboard",
    "price": 100,
    "stock": 10
  }
}
```

## Create Product

```json
{
  "message": "Product created successfully",
  "product": {
    "id": 1,
    "name": "Keyboard",
    "price": 100,
    "stock": 10
  }
}
```

The endpoint returns HTTP `201 Created`.

## Update Product

```json
{
  "message": "Product updated successfully",
  "product": {
    "id": 1,
    "name": "Keyboard",
    "price": 150,
    "stock": 20
  }
}
```

## Delete Product

```json
{
  "message": "Product deleted successfully"
}
```

---

# Error Handling

The API returns structured JSON error responses.

Example:

```json
{
  "error": "Product name is required",
  "status": 400
}
```

The HTTP status code is also returned appropriately.

### HTTP 400 Bad Request

Used for invalid client input, including:

* Missing JSON request body
* Missing product name
* Missing price
* Missing stock
* Negative price
* Negative stock
* Invalid price type
* Invalid stock type
* Boolean values used as price or stock
* Invalid pagination parameters
* Invalid sorting fields
* Invalid filter values

### HTTP 404 Not Found

A nonexistent product returns:

```json
{
  "error": "Product not found",
  "status": 404
}
```

The application uses a centralized Flask `404` error handler located in `app/errors/handlers.py`.

---

## Project Structure

```text

flask/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── errors/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── handlers.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── product_repository.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── general.py
│   │   └── products.py
│   └── services/
│       ├── __init__.py
│       └── product_service.py
├── config.py
├── Dockerfile
├── main.py
├── requirements.txt
└── tests/
    ├── conftest.py
    ├── __init__.py
    └── test_products.py

```

## Normal Application Execution

When the application is started with Docker Compose:

```bash
sudo docker compose up --build
```

the application starts through the Flask application factory.

The general startup flow is:

```text
Docker Compose
      │
      ▼
Flask Container
      │
      ▼
main.py
      │
      ▼
app.create_app()
      │
      ├── Load configuration
      ├── Configure database URI
      ├── Initialize SQLAlchemy
      ├── Register Blueprints
      ├── Register error handlers
      └── Create database tables
      │
      ▼
Flask Development Server
      │
      ▼
HTTP Requests
      │
      ▼
Routes / Blueprints
      │
      ▼
Service Layer
      │
      ▼
Repository Layer
      │
      ▼
SQLAlchemy / Models
      │
      ▼
MySQL
```

`main.py` is responsible for starting the application.

The application factory in `app/__init__.py` is responsible for application creation, configuration, extension initialization, Blueprint registration, error-handler registration, and database table creation.

Once the application is running, HTTP requests follow the layered architecture described in the Application Architecture section.

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

The tests use a dedicated test database:

```text
store_test
```

This keeps automated test data separate from the normal application database and prevents tests from modifying development data.

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

### `products`

Creates multiple products for tests involving pagination, searching, sorting, filtering, and combined query parameters.

```python
@pytest.fixture
def products(app):
    ...
```

### `clean_products`

Automatically removes test products after each test.

The test database is dedicated to automated testing, so clearing the product table after each test helps keep tests isolated and repeatable.

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

The current test suite contains:

```text
66 passing tests
```

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
* Search
* Sorting
* Filtering
* Combined query parameters
* Standardized error responses
* PUT/PATCH nonexistent product handling

---

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
docker pull bacharidocker/flask-product-api:v1.2.0
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

---

## GitHub Development Checkpoint 1 — Pagination

A dedicated development commit was created for the pagination feature.

Completed:

* Pagination with `page`
* Pagination with `per_page`
* Pagination validation
* Pagination metadata
* SQLAlchemy `limit()`
* SQLAlchemy `offset()`
* Pagination tests

---

## GitHub Development Checkpoint 2 — Testing Architecture

A second development commit focused on improving the testing architecture.

Completed:

* pytest setup
* Flask test client
* Application Factory pattern
* `TestingConfig`
* Dedicated test database
* pytest fixtures
* Automatic test cleanup
* Improved test organization
* Expanded API endpoint tests

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

---
## v1.2.0 — API Querying and Quality

Completed:

* Search
* Sorting
* Filtering
* Combined query parameters
* Improved validation
* Standardized error response structure
* Centralized HTTP 404 handling
* Consistent product response structure
* PUT/PATCH nonexistent product tests
* Expanded API test coverage
* **66  tests**

This release represents the completion of the current API querying and basic API quality phase.

---
## GitHub Development Checkpoint 3 — Application Architecture

A third development checkpoint focuses on refactoring the application architecture and separating application responsibilities.
Completed:

* Application Factory pattern
* Flask Blueprints
* Separate product and general routes
* Dedicated error-handling module
* Separated application entry point
* Service Layer
* Repository Layer
* Separation of HTTP, application, and database responsibilities
* Updated application package structure
* Updated test architecture
* Maintained 66 tests

Current architecture:
```text
Routes
  ↓
Service Layer
  ↓
Repository Layer
  ↓
SQLAlchemy / Models
  ↓
MySQL
```
Supporting components:

Extensions → Flask / SQLAlchemy setup
Errors     → Centralized error handling

The next step after completing the architecture checkpoint is to begin the DevOps learning track.

# Future Roadmap
## Professional API Architecture

Completed:
* Application Factory pattern
* Flask Blueprints
* Dedicated error-handling module
* Separated application entry point
* Service Layer
* Repository / data-access layer
* Separation of HTTP, application, and database responsibilities


Planned:
* Schemas and serialization
* Stronger request validation
* Environment-specific configuration
* Database migrations
* Further API architecture improvements

---

## Product Features

Planned:

* Product image uploads
* Image validation
* Image replacement
* Image cleanup
* Persistent image storage
* Product categories
* Product relationships

---

### Testing and API Quality

Planned:

* Further test organization
* API contract testing
* Additional edge-case testing
* Code quality improvements
* Test coverage improvements

---
DevOps Learning Track

## The DevOps track will be developed separately from the main API development path.

Planned topics:

* Git and branching workflow
* Docker fundamentals
* Dockerfile deeper understanding
* Docker Compose
* Container networking
* Docker volumes
* Container registries
* CI/CD fundamentals
* GitHub Actions
* Automated testing pipelines
* Docker image builds and publishing
* Kubernetes fundamentals
* Kubernetes deployments
* Kubernetes Services
* ConfigMaps
* Secrets
* Persistent Volumes
* Persistent Volume Claims
* Ingress
* Health probes
* Resource requests and limits
* kubectl
* Kubernetes troubleshooting
* Helm
* Terraform
* Ansible
* Logging and monitoring
* Observability

Kubernetes will be introduced after the Docker and CI/CD fundamentals are understood.

## Authentication and Security

Planned:

* Authentication
* Authorization
* Password hashing
* JWT access tokens
* Roles and permissions
* CORS
* Security best practices
* SQL injection protection

---

### Docker and Production

Planned:

* Gunicorn
* Nginx
* Production Docker image
* Database migrations
* Container optimization
---
## Cloud

Planned:

Cloud fundamentals
Compute
Networking
Managed databases
Container registries
Secrets management
API deployment


## CI/CD

Planned:

GitHub Actions
Automated tests
Docker image builds
Docker image publishing
Deployment pipelines
Automated deployment


## Production and Advanced Features
Planned:

Logging
Monitoring
Observability
Performance optimization
Caching
Database optimization
Rate limiting
Security hardening
Production deployment

---

# Docker Image

The application image is available on Docker Hub:

https://hub.docker.com/r/bacharidocker/flask-product-api
---

The v1.2.0 image can be pulled with:

```bash
docker pull bacharidocker/flask-product-api:v1.2.0
```
---
## Author

**Hossein Bachari**

GitHub: https://github.com/bacharigit
