#!/bin/sh

docker run \
  --rm   \
  --name postgres-fastapi \
  -p 5432:5432 \
  -e POSTGRES_USER=link \
  -e POSTGRES_PASSWORD=link \
  -e POSTGRES_DB=link \
  -d \
  postgres:16
