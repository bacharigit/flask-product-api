# Flask Product API

A Flask REST API for managing products, backed by MySQL and SQLAlchemy.

This project is also used as a practical DevOps learning project, covering containerization, testing, CI/CD, Docker image publishing, and automated deployment.

---

## Project Architecture

### Development

```text
Developer machine
      |
      | docker compose
      v
+-----------------------+
| Flask API             |
| Gunicorn              |
+-----------------------+
          |
          v
+-----------------------+
| MySQL 8.0             |
+-----------------------+
          |
          v
   Docker named volume
```

### CI/CD

```text
Git push / Pull Request
          |
          v
   GitHub Actions
          |
          +----> Run tests
          |
          +----> Build runtime image
          |
          +----> Test container
          |
          +----> Test production SSH
          |
          +----> On version tag:
                    |
                    v
              Push image to
                Docker Hub
                    |
                    v
              Deploy to
            production server
```

### Production Lab

```text
GitHub Actions
      |
      | SSH
      v
192.168.1.104
Production server
      |
      +------------------+
      |                  |
      v                  v
 Flask container     MySQL container
      |                  |
      +------------------+
               |
          mysql-data
        Docker volume
```

---

## Technologies

### Application

* Python
* Flask
* SQLAlchemy
* MySQL
* Pytest
* Gunicorn

### DevOps

* Docker
* Docker Compose
* GitHub Actions
* Docker Hub
* SSH
* Linux

---

## Project Structure

```text
project-root/
├── .gitignore
├── .env
├── .env.example
├── docker-compose.yml
├── compose.production.yml
├── README.md
├── flask/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── main.py
│   ├── config.py
│   ├── app/
│   └── tests/
└── mysql/
    └── init/
        └── 00-create-test-db.sql
```

---

# Local Development

## Requirements

* Docker
* Docker Compose

The application and tests run inside Docker containers.

Python and pytest do not need to be installed on the host machine.

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```dotenv
DB_NAME=store
DB_PASSWORD=your-password
```

Do not commit `.env`.

Use `.env.example` as the safe template.

---

## Start the Development Stack

```bash
docker compose up -d
```

This starts:

* Flask
* MySQL

MySQL has a healthcheck, and Flask waits for MySQL to become healthy.

Check the containers:

```bash
docker compose ps
```

---

## Test the API

```bash
curl http://localhost:5000/api/hello
```

Products:

```bash
curl http://localhost:5000/api/products
```

---

# Running Tests

Tests run inside the Docker test image.

```bash
docker compose run --rm flask-test
```

The test image uses the `test` target in the multi-stage Dockerfile.

The test environment uses a separate database:

```text
store_test
```

The test database is created by:

```text
mysql/init/00-create-test-db.sql
```

---

# Docker Image

The Flask Dockerfile uses multiple build stages:

```text
base
 |
 +----> test
 |
 +----> runtime
```

The runtime image:

* Uses Gunicorn
* Runs as a non-root user
* Does not contain development dependencies
* Exposes port `5000`

The application is started with:

```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

The Docker image is published to:

```text
bacharidocker/flask-product-api
```

---

# CI/CD

GitHub Actions is used for continuous integration and deployment.

## Pipeline

```text
test
  |
  v
build
  |
  +------------------+
  |                  |
  v                  v
deploy-test       publish
                     |
                     v
                   deploy
```

### On normal branch pushes

```text
test
  ↓
build
  ↓
deploy-test
```

The Docker image is built and the production SSH connection is tested.

The Docker image is not published.

### On version tags

For example:

```bash
git tag v1.4.0
git push origin v1.4.0
```

The pipeline performs:

```text
test
  ↓
build
  ↓
publish Docker image
  ↓
deploy to production
```

---

# Docker Hub

Versioned images are published to:

```text
bacharidocker/flask-product-api
```

Example:

```text
bacharidocker/flask-product-api:v1.3.1
```

The production server pulls a specific version rather than building the application from source.

---

# Production Deployment

Production uses:

```text
compose.production.yml
```

Unlike the development Compose file, the production configuration uses a pre-built Docker image:

```yaml
image: bacharidocker/flask-product-api:${IMAGE_TAG}
```

The production server does not need the application source code.

It only needs:

* Docker
* Docker Compose
* Production environment variables
* Access to the Docker image

---

## Production Directory

The production deployment is located at:

```text
/opt/flask-product-api
```

Example:

```text
/opt/flask-product-api/
├── compose.production.yml
├── deploy.sh
└── .env
```

The production `.env` contains:

```dotenv
DB_NAME=store
DB_PASSWORD=your-production-password
```

The production environment file must not be committed to Git.

---

# Deployment Script

Production deployments are performed with:

```bash
./deploy.sh <image-tag>
```

For example:

```bash
./deploy.sh v1.3.1
```

The script:

1. Receives the image tag.
2. Pulls that version from Docker Hub.
3. Starts/recreates the production containers.
4. Displays the resulting container status.

Example:

```bash
./deploy.sh v1.4.0
```

---

# Rollback

Because production uses versioned Docker images, rollback does not require rebuilding the application.

For example, if `v1.4.0` has a problem:

```bash
./deploy.sh v1.3.1
```

This allows the production environment to return to the previous known-good image.

---

# Security Practices

The project intentionally avoids committing secrets.

Sensitive values are stored outside Git:

```text
.env
```

The repository contains:

```text
.env.example
```

instead.

The production `.env` should have restrictive permissions:

```bash
chmod 600 .env
```

The production Flask container also runs as a non-root Linux user:

```text
appuser
```

---

# Git Branches

The project uses separate branches for application development and DevOps learning.

```text
main
 |
 | stable application development
 |
devops-learning
 |
 +-- Docker
 +-- CI/CD
 +-- Docker Hub
 +-- deployment
 +-- production lab
```

DevOps changes are developed on:

```text
devops-learning
```

---

# Versioning

The project uses Git tags for releases.

Example:

```bash
git tag v1.4.0
git push origin v1.4.0
```

A version tag triggers the Docker image publishing and production deployment workflow.

---

# Current DevOps Milestone

## v1.4.0

The `v1.4.0` milestone represents the automated CI/CD deployment pipeline.

Implemented:

* Dockerized Flask application
* Multi-stage Docker build
* Separate test and runtime images
* Non-root runtime container
* Docker Compose development environment
* MySQL healthcheck
* Automated pytest execution
* GitHub Actions CI
* Docker runtime verification
* Docker Hub publishing
* Self-hosted GitHub Actions runner
* SSH deployment to production lab
* Production Docker Compose configuration
* Versioned Docker image deployment
* Automated production deployment
* Deployment rollback using image tags

---

# Future DevOps Roadmap

Planned improvements:

1. Automated rollback testing
2. Cloud VM deployment
3. GitHub-hosted runner → cloud VM deployment
4. Nginx reverse proxy
5. HTTPS with Let's Encrypt
6. Application healthchecks
7. Centralized logging
8. Monitoring
9. Kubernetes
10. Kubernetes Deployments and Services
11. ConfigMaps and Secrets
12. Persistent Volumes
13. Helm
14. Kubernetes-based CI/CD

---

## API

The application provides product-related REST API endpoints.

Example:

```bash
curl http://localhost:5000/api/products
```

For development, start the application with:

```bash
docker compose up -d
```

Then access the API on:

```text
http://localhost:5000
```
