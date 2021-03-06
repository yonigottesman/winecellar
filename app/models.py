from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.event import listens_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.common import file_path, silentremove


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    wines = db.relationship(
        "Wine", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    rating = db.Column(db.Integer, default=0)
    file_name = db.Column(db.String(140))

    def __repr__(self):
        return "<Wine {}>".format(self.body)


@listens_for(Wine, "after_delete")
def on_delete(mapper, connection, wine):
    if wine.file_name:
        silentremove(file_path(wine.file_name))
