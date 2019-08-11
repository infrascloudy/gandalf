import os


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_precious"


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if "TRAVIS" in os.environ:
        SQLALCHEMY_DATABASE_URI = (
            "postgres://gandalf:gandalf@localhost:5432/gandalf_test"
        )


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    if "TRAVIS" in os.environ:
        SQLALCHEMY_DATABASE_URI = (
            "postgres://gandalf:gandalf@localhost:5432/gandalf_test"
        )


class ProductionConfig(BaseConfig):
    """Production configuration"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if "TRAVIS" in os.environ:
        SQLALCHEMY_DATABASE_URI = (
            "postgres://gandalf:gandalf@localhost:5432/gandalf_test"
        )
