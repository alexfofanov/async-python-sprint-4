FROM python:3.11
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
COPY ./migrations /app/migrations
COPY alembic.ini /app
COPY .env_docker /app/.env
COPY alembic.ini /app
EXPOSE 8000
CMD ["fastapi", "run", "src/main.py", "--port", "8000"]
