FROM python:3.11
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src ./src
COPY ./migrations ./migrations
COPY alembic.ini .
COPY .env_docker .env
COPY alembic.ini .
EXPOSE 8000
CMD ["fastapi", "run", "src/main.py", "--port", "8000"]
