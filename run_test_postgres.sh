#!/bin/sh

docker run \
  --rm   \
  --name postgres-fastapi-test \
  -p 6432:5432 \
  -e POSTGRES_USER=link \
  -e POSTGRES_PASSWORD=link \
  -e POSTGRES_DB=link_test \
  -d \
  postgres:16
