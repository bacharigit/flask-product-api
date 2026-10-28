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
.
├── compose.logging.yml
├── compose.monitoring.yml
├── compose.production.yml
├── deploy.sh
├── docker-compose.yml
├── README.md
├── flask/
│   ├── app/
│   │   ├── errors/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   └── services/
│   ├── config.py
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements-dev.txt
│   ├── requirements.txt
│   └── tests/
├── logging/
│   ├── filebeat/
│   │   └── filebeat.yml
│   └── logstash/
│       └── pipeline/
│           └── logstash.conf
├── monitoring/
│   ├── Dockerfile
│   ├── health_check.py
│   └── prometheus/
│       └── prometheus.yml
├── mysql/
│   └── init/
│       └── 00-create-test-db.sql
└── nginx/
    └── default.conf
```

**Note:** The tree shows the main project files and configuration. Local TLS certificates, generated log files, and temporary test utilities are omitted intentionally.



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

# Nginx Reverse Proxy and Troubleshooting

## Overview

Nginx is used as a reverse proxy in an isolated DevOps learning environment.

It receives HTTP requests from clients and forwards them to the Flask API running inside Docker Compose.

```text
Client
  |
  | HTTP :8080
  v
Nginx container
  |
  | Docker network
  v
Flask container :5000
  |
  v
MySQL container
```

The lab exposes Nginx on host port `8080` because port `80` is already in use on the development machine.

Nginx configuration:

```text
nginx/default.conf
```

## Reverse Proxy Configuration

The Nginx configuration forwards incoming requests to the Flask service:

```nginx
location / {
    proxy_pass http://flask:5000;
}
```

The hostname `flask` resolves to the Flask service through the Docker Compose network.

The configuration also forwards request headers and defines proxy timeouts.

## Service Health Checks

The Flask container has a Docker health check that requests:

```text
http://127.0.0.1:5000/api/hello
```

The check helps Docker distinguish between a running container and an application that responds successfully to the health-check request.

Nginx uses the following Compose dependency:

```yaml
depends_on:
  flask:
    condition: service_healthy
```

This makes Compose wait for Flask to become healthy before starting Nginx during startup.

A health check detects failures but does not, by itself, restart an unhealthy container.

## Running the Nginx Lab

Start the isolated lab using the versioned Flask image:

```bash
IMAGE_TAG=v1.4.2 docker compose -p nginx-lab \
  --env-file .env \
  -f compose.production.yml up -d
```

Check service status:

```bash
IMAGE_TAG=v1.4.2 docker compose -p nginx-lab \
  --env-file .env \
  -f compose.production.yml ps
```

Test the API through Nginx:

```bash
curl -i http://localhost:8080/api/hello
```

Expected result:

```text
HTTP/1.1 200 OK
```

## Nginx Logging

View Nginx access and error logs through Docker Compose:

```bash
IMAGE_TAG=v1.4.2 docker compose -p nginx-lab \
  --env-file .env \
  -f compose.production.yml logs --tail=30 nginx
```

Access logs record HTTP requests and their response status codes.

Examples observed during testing:

- `200 OK`: the API request succeeded.
- `404 Not Found`: the requested endpoint does not exist.
- `502 Bad Gateway`: often indicates an upstream connection failure or invalid upstream response.
- `504 Gateway Timeout`: an upstream operation timed out.

## Failure Testing and Recovery

A backend failure was simulated by stopping the Flask service:

```bash
docker compose -p nginx-lab \
  --env-file .env \
  -f compose.production.yml stop flask
```

A request to the API then returned `504 Gateway Timeout` in this lab. The Nginx error log reported an upstream connection timeout.

Flask was started again:

```bash
IMAGE_TAG=v1.4.2 docker compose -p nginx-lab \
  --env-file .env \
  -f compose.production.yml up -d flask
```

The API was tested again and returned `200 OK`.

### Lessons Learned

- Nginx acts as a reverse proxy for the Flask API.
- Docker Compose service names can be used for communication between containers on the same network.
- Health checks monitor application responsiveness.
- Compose startup dependencies can wait for a service to become healthy.
- Access logs show request outcomes; error logs help explain failures.
- Backend recovery should be verified by testing the API again.

**Note:** The `nginx-lab` Compose project is an isolated learning environment. Changes to `compose.production.yml` must be reviewed before they are used for an actual production deployment.
## HTTPS with a Self-Signed Certificate

### Overview

The Nginx reverse proxy supports both HTTP and HTTPS in the local development lab.

- HTTP endpoint: `http://localhost:8080`
- HTTPS endpoint: `https://localhost:8443`
- Nginx listens on container ports `80` (HTTP) and `443` (HTTPS).
- Docker Compose maps host port `8080` to Nginx port `80`, and host port `8443` to Nginx port `443`.
- Nginx terminates TLS and forwards requests to the Flask application over the internal Docker network using HTTP at `flask:5000`.

### Certificate generation

A self-signed certificate was generated using OpenSSL for local testing.

The certificate includes these Subject Alternative Names (SANs):

- `DNS:localhost`
- `IP Address:127.0.0.1`

The local certificate files are stored in `nginx/certs/`:

- `localhost.crt`: the certificate presented by Nginx.
- `localhost.key`: the corresponding private key.

The certificate directory and private key files are excluded from Git using `.gitignore`. **Never commit private keys to the repository.**

To inspect the certificate:

```bash
openssl x509 -in nginx/certs/localhost.crt \
  -noout -subject -issuer -dates -ext subjectAltName
```

### Testing HTTP and HTTPS

Test the HTTP endpoint:

```bash
curl -I http://localhost:8080/api/hello
```

Test HTTPS with normal certificate verification:

```bash
curl -I https://localhost:8443/api/hello
```

Because the certificate is self-signed and is not trusted by default, this request normally fails certificate verification.

For local testing, explicitly trust the generated certificate:

```bash
curl --cacert nginx/certs/localhost.crt \
  -I https://localhost:8443/api/hello
```

This should return `HTTP/1.1 200 OK` when the services are running correctly.

The `-k` option can also bypass certificate verification:

```bash
curl -k -I https://localhost:8443/api/hello
```

Use `-k` only for temporary troubleshooting. It disables certificate verification and should not be used as a production solution.

### Verifying TLS

Verify the certificate presented by Nginx:

```bash
openssl s_client \
  -connect localhost:8443 \
  -servername localhost \
  -CAfile nginx/certs/localhost.crt \
  -verify_return_error </dev/null
```

A successful verification should report:

```text
Verify return code: 0 (ok)
```

### Troubleshooting

- **Connection refused:** Check that the Nginx container is running and host port `8443` is published.
- **Certificate is self-signed:** Use the local certificate with `curl --cacert` for testing.
- **Nginx fails to start:** Inspect Nginx logs and verify that the certificate and private key paths are correct.
- **502 or 504 response:** Check whether Flask is healthy and reachable through the Compose network, then inspect Nginx error logs.

### Security notes

- The certificate is self-signed and intended for local development only.
- The private key must remain secret and must not be committed to Git.
- `curl -k` disables certificate verification and does not establish that the server's identity is trusted.
- A public deployment should use a certificate issued by a trusted certificate authority, with a valid domain and appropriate renewal procedures.
- HTTPS protects traffic between the client and Nginx. In this configuration, traffic from Nginx to Flask uses HTTP over the internal Docker network.


## Monitoring: Prometheus, Grafana, and cAdvisor

This project includes a separate monitoring stack for observing container resource usage and monitoring Prometheus scrape targets.

### Architecture

- **Prometheus** collects metrics every 15 seconds.
- **cAdvisor** exposes container resource metrics, including CPU and memory usage.
- **Grafana** visualizes metrics and evaluates alert rules.

### Start the monitoring stack

From the project root, run:

```bash
docker compose -p monitoring-lab -f compose.monitoring.yml up -d
```

### Access the services

| Service | Local URL |
|---|---|
| Prometheus | http://localhost:9090 |
| Prometheus targets | http://localhost:9090/targets |
| Grafana | http://localhost:3000 |
| cAdvisor metrics | http://localhost:8081/metrics |

These ports are intended for the local development lab. Do not expose the monitoring services publicly without appropriate access controls.

### Grafana setup

1. Sign in to Grafana and change the default password when prompted.
2. Add Prometheus as a data source using `http://prometheus:9090`.
3. Create a dashboard with panels for target status, container memory usage, and container CPU usage.
4. Create an alert rule named `cAdvisor Target Down` using the PromQL expression:

   ```promql
   up{job="cadvisor"}
   ```

   Configure the rule to trigger when the value is below `1`.

### Verify monitoring

Check the Prometheus targets page and confirm both the Prometheus and cAdvisor targets are `UP`.

Test alerting by stopping cAdvisor:

```bash
docker compose -p monitoring-lab -f compose.monitoring.yml stop cadvisor
```

Confirm that the `CAdvisor Target Down` alert fires in Grafana. Restore the service afterward:

```bash
docker compose -p monitoring-lab -f compose.monitoring.yml start cadvisor
```

After Prometheus detects recovery, verify that the alert returns to `Normal`.

### Stop the monitoring stack

```bash
docker compose -p monitoring-lab -f compose.monitoring.yml down
```

Named volumes preserve Prometheus and Grafana data when the stack is stopped this way. To remove the volumes as well, use `down -v`; this deletes the monitoring stack's persisted data.

### Important notes

- The monitoring stack runs as a separate Compose project named `monitoring-lab`.
- The cAdvisor configuration uses elevated privileges and read-only host mounts for local container monitoring. Treat this setup as a development lab, not a production security baseline.
- An alert entering the `Firing` state does not guarantee that email delivery works; SMTP must be configured and tested separately.


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

# Monitoring, Logging, and Alerting

## Prometheus and Grafana

**Status: Implemented and tested in the local lab**

- Prometheus metrics collection and target monitoring
- cAdvisor container resource metrics
- Grafana dashboards for monitoring
- Alert rule for detecting a down cAdvisor target
- Tested alert behavior by stopping and restoring cAdvisor

## ELK Stack

**Status: Implemented and tested in the local lab**

- Filebeat collects Docker and health-check logs
- Logstash processes logs and forwards them to Elasticsearch
- Elasticsearch stores indexed log data
- Kibana dashboards visualize API health, response times, and failed health checks
- Kibana alert rules detect API downtime and slow responses
- Tested alert conditions by simulating API failures and slow responses
- Configured and tested a Server log connector for alert actions

**Remaining improvements:** External notifications such as email, Slack, or Microsoft Teams, plus improved incident response documentation.

# Future DevOps Roadmap

**Status: Core lab implemented**

- Prometheus and Grafana for container monitoring and dashboards
- cAdvisor metrics and Prometheus target monitoring
- Centralized logging with Elasticsearch, Logstash, Filebeat, and Kibana
- Kibana dashboards for API health, response times, and failed health checks
- Kibana alert rules for API downtime and slow responses
- Server log connector configured and tested for alert actions
- Failure simulation, log investigation, and recovery validation

**Remaining improvements:**
- Configure external notifications such as email, Slack, or Microsoft Teams
- Improve alert documentation and incident response procedures

## 2. Ansible

**Status: Next stage**

- Set up an Ansible control node and managed Linux hosts
- Configure inventory, SSH access, and privilege escalation
- Learn ad-hoc commands, playbooks, variables, facts, and templates
- Use handlers, roles, and reusable task structures
- Practice idempotency, check mode, and safe configuration changes
- Automate Linux host preparation, Docker installation, and Docker Compose configuration
- Automate application deployment to the private lab
- Validate deployments and integrate Ansible with the existing CI/CD pipeline where appropriate

## 3. Production Readiness and Security

- Review SSH access, firewall rules, and least-privilege permissions
- Manage secrets safely and separate development from production configuration
- Implement and test database backup and recovery procedures
- Validate health checks, deployment rollback, and service recovery
- Review reverse-proxy configuration and HTTPS certificate management
- Improve monitoring, logging, alerting, and troubleshooting documentation

## 4. Kubernetes

- Set up a local Kubernetes environment using kind, Minikube, or k3d
- Learn Pods, Deployments, and Services
- Configure ConfigMaps and Secrets
- Work with Persistent Volumes and Persistent Volume Claims
- Configure health probes, resource requests, and limits
- Practice networking, application troubleshooting, and Helm
- Deploy the Flask API and integrate Kubernetes deployment with CI/CD

## 5. Terraform and Cloud Infrastructure

- Learn Terraform providers, resources, variables, outputs, and state
- Organize infrastructure with reusable modules
- Provision infrastructure using Infrastructure as Code
- Combine Terraform provisioning with Ansible configuration management
- Plan cloud deployment, networking, access controls, and cost management
- Deploy to a cloud VM when the local and private-lab work is ready

## 6. Advanced Integrations and Portfolio

- Integrate deployment and monitoring workflows
- Explore external alert notifications and incident automation
- Document architecture, setup, troubleshooting, rollback, and recovery
- Improve the project README and operational runbooks
- Prepare a reproducible end-to-end DevOps portfolio demonstration

**Guiding principle:** Complete and validate as much as possible in the existing local and private lab before introducing public cloud infrastructure. Cloud deployment and final end-to-end validation come later.




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
