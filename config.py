import os

from flask import json


class Config:
    # Database settings/credentials
    DB_HOST = os.getenv("DB_HOST", "docker-db")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "mydatabase")
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://user:password@db:5432/mydatabase"
    )

    # Swagger variables
    SWAGGER_URL = os.getenv("SWAGGER_URL", "/swagger-ui")
    SWAGGER_API_URL = os.getenv("SWAGGER_API_URL", "/swagger")

    # Variables needed for testing/development
    TEST_HOST = os.getenv("TEST_HOST", "localhost")
    TEST_PORT = json.loads(
        os.getenv("TEST_PORT", "5000"), **{"parse_float": float, "parse_int": int}
    )
