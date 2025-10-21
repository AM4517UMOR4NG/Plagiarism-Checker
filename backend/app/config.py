import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "development")
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/plagiarism")

    s3_endpoint: str = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    s3_access_key: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    s3_secret_key: str = os.getenv("S3_SECRET_KEY", "minioadmin")
    s3_bucket: str = os.getenv("S3_BUCKET", "plagiarism")
    s3_region: str = os.getenv("S3_REGION", "us-east-1")
    s3_use_ssl: bool = os.getenv("S3_USE_SSL", "false").lower() == "true"

    elasticsearch_url: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")

    jwt_secret: str = os.getenv("JWT_SECRET", "change_me")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")


settings = Settings()
