import uuid
from app.db import db
from flask_login import UserMixin
from app.utils.password_utils import hash_password, check_password

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(24))
    last_name = db.Column(db.String(24))
    username = db.Column(db.String(24), index=True, unique=True)
    email = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(128))
    birth_date = db.Column(db.Date)
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    role = db.Column(db.String(20), default='Reader') 
    is_verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def __repr__(self):
        return f'<User {self.username}>'
