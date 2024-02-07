"""Config."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Config class to load environment variables."""

    def __init__(self) -> None:
        self.DB_HOST = os.environ.get("DB_HOST")
        self.DB_PORT = os.environ.get("DB_PORT")
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_USER = os.environ.get("DB_USER")
        self.DB_PASS = os.environ.get("DB_PASS")
