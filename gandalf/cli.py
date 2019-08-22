import sys
import coverage
import unittest

from gandalf import db
from gandalf.database.models.user import User


COV = coverage.coverage(
    branch=True, include="gandalf/*", omit=["gandalf/tests/*", "gandalf/config.py"]
)
COV.start()


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
