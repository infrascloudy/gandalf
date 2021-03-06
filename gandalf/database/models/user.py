from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

from gandalf import db
from gandalf.database.uuid_type import UUID


class User(db.Model):

    id = db.Column(UUID, primary_key=True, nullable=False)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(100))
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
        }

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
