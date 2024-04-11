# app/config.py
from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database_name: str = "dummy-api"

    class Config:
        # Assuming your .env file is in the project root directory,
        # you may need to provide an absolute path depending on your setup
        env_file = ".env"

settings = Settings()
