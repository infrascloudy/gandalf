# -*- coding: utf-8 -*-
"""Blazingly fast & beautifully expressive Web Apps and APIs"""
import os
import sys
import unittest
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import coverage

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), "..")  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

COV = coverage.coverage(
    branch=True, include="gandalf/*", omit=["gandalf/tests/*", "gandalf/config.py"]
)
COV.start()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

from gandalf.models.user import User


def create_app(script_info=None):
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_blueprints(app)
    register_commands(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


def register_blueprints(app):
    from gandalf.api.auth import auth_blueprint
    from gandalf.api.users import users_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)


def register_commands(app):
    @app.cli.command("recreate_db")
    def recreate_db():
        """Recreate the database."""
        db.drop_all()
        db.create_all()
        db.session.commit()

    @app.cli.command("test")
    def test():
        """Runs the tests without code coverage"""
        tests = unittest.TestLoader().discover("gandalf/tests", pattern="test*.py")
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        sys.exit(result)

    @app.cli.command("seed_db")
    def seed_db():
        """Seeds the database."""
        db.session.add(User(username="michael", email="hermanmu@gmail.com"))
        db.session.add(User(username="michaelherman", email="michael@mherman.org"))
        db.session.commit()

    @app.cli.command("cov")
    def cov():
        """Runs the unit tests with coverage."""
        tests = unittest.TestLoader().discover("gandalf/tests")
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            COV.stop()
            COV.save()
            print("Coverage Summary:")
            COV.report()
            COV.html_report()
            COV.erase()
            return 0
        sys.exit(result)
