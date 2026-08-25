# Flask Product REST API

> **Version:** v1.0.0

A Flask REST API for managing products using **Flask**, **MySQL**, **SQLAlchemy**, **Docker**, and **Docker Compose**.

This project provides product CRUD operations through a REST API using JSON instead of server-rendered HTML pages.

---

## Features

* Product CRUD operations
* JSON responses
* GET products
* POST products
* PUT products
* PATCH products
* DELETE products
* Input validation
* Error handling
* MySQL database
* SQLAlchemy ORM
* Docker
* Docker Compose
* Environment variables
* MySQL health check

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
* Docker
* Docker Compose

---

## Relationship to the Previous Project

This project is the REST API evolution of the previous **Flask Store CRUD** application.

The previous project used server-rendered HTML pages with Jinja2 templates.

This project replaces the HTML-based interface with a REST API that communicates using JSON.

The project continues to use MySQL and SQLAlchemy for product data management.

---

## Project Structure

```text
.
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
│
└── flask
    ├── Dockerfile
    ├── main.py
    ├── models.py
    └── requirements.txt
```

> The `.env` file is intentionally not included in the repository because it contains sensitive configuration.

---

## Docker

The application runs with Docker Compose using two containers:

* Flask API
* MySQL 8.0

The Flask container communicates with the MySQL container through the Docker Compose network.

### Start the application

First, create the environment file from the example:

```bash
cp .env.example .env
```

Edit `.env` and provide your database configuration.

Then build and start the application:

```bash
sudo docker compose up --build
```

The API is available at:

```text
http://localhost:5000
```

Test the API:

```text
http://localhost:5000/api/hello
```

### Stop the application

Press:

```text
Ctrl+C
```

or run:

```bash
sudo docker compose down
```

### MySQL health check

The MySQL container includes a health check to verify that MySQL is ready to accept connections.

The database data is stored in a named Docker volume:

```yaml
volumes:
  - mysql-data:/var/lib/mysql
```

This allows the MySQL data to persist when containers are stopped or recreated.

---

## Environment Configuration

Sensitive configuration is stored in a local `.env` file.

The `.env` file is ignored by Git and should never be committed to GitHub.

Create the `.env` file from the provided example:

```bash
cp .env.example .env
```

Example `.env`:

```env
DB_PASSWORD=your-database-password
DB_NAME=store
```

The Flask application receives these values through environment variables.

The MySQL container uses the same environment variables to configure the database.

The repository contains `.env.example` as a safe configuration template.

---

## Testing

The API can be tested using `curl` from the terminal.

### Test the API

```bash
curl http://localhost:5000/api/hello
```

Expected response:

```json
{
  "message": "Hello from Flask API"
}
```

### Get all products

```bash
curl http://localhost:5000/api/products
```

### Get one product

```bash
curl http://localhost:5000/api/products/1
```

### Create a product

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"keyboard","price":100,"stock":15}'
```

### Replace a product with PUT

PUT requires the complete product data:

```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"mechanical keyboard","price":150,"stock":20}'
```

### Partially update a product with PATCH

PATCH can update only the fields that are provided:

```bash
curl -X PATCH http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price":175}'
```

### Delete a product

```bash
curl -X DELETE http://localhost:5000/api/products/1
```

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

### v1.0.0

* Initial Flask REST API
* Product CRUD operations
* GET, POST, PUT, PATCH, and DELETE endpoints
* MySQL integration
* SQLAlchemy ORM
* JSON responses
* Input validation
* Error handling
* Docker Compose support
* MySQL health check
* Environment variable configuration

---

## Future Improvements

Planned features:

* User authentication
* API documentation with Swagger/OpenAPI
* Automated tests
* Better project structure
* Pagination
* Search and filtering
* Product images
* Database migrations
* Improved error handling
* CI/CD with GitHub Actions

---

## Author

**Hossein Bachari**

GitHub: https://github.com/bacharigit
