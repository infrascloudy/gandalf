from gandalf import db
from gandalf.models.user import User


def add_user(username, email, password):
    user = User(username=username, email=email)
    user.password = password
    db.session.add(user)
    db.session.commit()
    return user
