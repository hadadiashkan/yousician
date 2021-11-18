import os

from dotenv import load_dotenv


class Config(object):
    """
    Default Configuration
    """

    load_dotenv()
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    SECRET_KEY = os.getenv("SECRET_KEY")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR")

    MONGODB_SETTINGS = {
        "db": os.getenv("MONGODB_DB"),
        "host": os.getenv("MONGODB_HOST"),
        "port": int(os.getenv("MONGODB_PORT")),
    }

    INSTALLED_RESOURCES = [
        "song",
    ]

    # To enable flask to catch package exceptions
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(Config):
    """
    Development Configuration
    """

    DEBUG = True


class DeploymentConfig(Config):
    """
    Deployment Configuration
    """

    DEBUG = False


# class TestingConfig(Config):
#     """
#     Test Configuration
#     """
#
#     DB_SERVER = "localhost"
#     DEBUG = False
#     TESTING = True
#     MONGODB_SETTINGS = {
#         "db": os.getenv("TEST_MONGODB_DB"),
#         "host": os.getenv("TEST_MONGODB_HOST"),
#         "port": int(os.getenv("TEST_MONGODB_PORT")),
#     }
#
#     SECRET_KEY = os.getenv("TEST_SECRET_KEY")
#     UPLOAD_DIR = os.getenv("TEST_UPLOAD_DIR")
