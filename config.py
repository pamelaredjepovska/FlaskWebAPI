import os


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://user:password@db:5432/flask_api_db"
    )
