import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME: str = "FastAPI Auth Backend"
SECRET_KEY: str = "your-secret-key"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
DATABASE_URL: str = "postgresql://user:password@localhost/dbname"

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
