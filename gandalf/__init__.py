# -*- coding: utf-8 -*-
"""Blazingly fast & beautifully expressive Web Apps and APIs"""
import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), "..")  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)



db = SQLAlchemy()
migrate = Migrate()


def create_app(script_info=None):
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    import_extras(app)

    return app


def register_blueprints(app):
    from gandalf.api.auth import auth_blueprint
    from gandalf.api.users import users_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)


def import_extras(app):
    from gandalf.cli import register_commands
    register_commands(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}
