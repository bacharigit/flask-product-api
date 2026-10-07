#!/usr/bin/env bash

set -e

cd /opt/flask-product-api

if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh <image-tag>"
    exit 1
fi

IMAGE_TAG="$1"

echo "Deploying image: bacharidocker/flask-product-api:${IMAGE_TAG}"

IMAGE_TAG="$IMAGE_TAG" docker compose \
  --env-file .env \
  -f compose.production.yml \
  pull flask

IMAGE_TAG="$IMAGE_TAG" docker compose \
  --env-file .env \
  -f compose.production.yml \
  up -d

echo "Waiting for Flask application..."

for i in {1..30}; do
    if curl --fail --silent http://localhost:5000/api/hello > /dev/null; then
        echo "Flask application is healthy"
        break
    fi

    echo "Waiting for Flask application... ($i/30)"
    sleep 2
done

if ! curl --fail --silent http://localhost:5000/api/hello > /dev/null; then
    echo "Deployment failed: Flask application is not responding"
    echo
    echo "Flask logs:"
    IMAGE_TAG="$IMAGE_TAG" docker compose \
      --env-file .env \
      -f compose.production.yml \
      logs flask
    exit 1
fi

echo "Deployment complete"


RUNNING_IMAGE=$(docker inspect \
    "$(docker compose --env-file .env -f compose.production.yml ps -q flask)" \
    --format '{{.Config.Image}}')

echo "Running image: ${RUNNING_IMAGE}"
echo

IMAGE_TAG="$IMAGE_TAG" docker compose \
  --env-file .env \
  -f compose.production.yml \
  ps
