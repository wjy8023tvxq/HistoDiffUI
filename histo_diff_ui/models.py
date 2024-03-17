from flask_login import UserMixin
from flask import session
from app import app, login_manager
from histo_diff_ui import db_utils
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = db_utils.get_db(app)
class User(UserMixin):
    def __init__(self, username, email, password_hash, _id):

        self.username = username
        self.email = email
        self.password_hash= password_hash
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self._id

    @classmethod
    def get_by_username(cls, username):
        data = db.find_one("users", {"username": username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_email(cls, email):
        data = db.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = db.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    @staticmethod
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.get_by_id(user_id)
        if user is not None:
            return User(user["_id"])
        else:
            return None

    @classmethod
    def register(cls, username, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(username, email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    def json(self):
        return {
            "username": self.username,
            "email": self.email,
            "_id": self._id,
            "password": self.password_hash
        }

