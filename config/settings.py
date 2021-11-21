# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from os import environ, getenv, path, urandom

from dotenv import load_dotenv


class Config(object):
    """
    Application Configuration
    """

    load_dotenv()
    BASE_DIR = path.dirname(path.dirname(__file__))

    ENV = environ.get("FLASK_ENV", default="production")
    DEBUG = ENV == "development"

    UPLOAD_DIR = getenv("UPLOAD_DIR")

    MONGODB_SETTINGS = {
        "db": getenv("MONGODB_DB"),
        "host": getenv("MONGODB_HOST"),
        "port": int(getenv("MONGODB_PORT")),
    }

    INSTALLED_RESOURCES = [
        "song",
    ]

    # To enable flask to catch package exceptions
    PROPAGATE_EXCEPTIONS = True

    SECRET_KEY = urandom(24)
    SEND_FILE_MAX_AGE_DEFAULT = getenv("SEND_FILE_MAX_AGE_DEFAULT")
