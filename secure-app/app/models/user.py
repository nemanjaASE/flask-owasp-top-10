from app import db
from flask_login import UserMixin
from app import login_manager
from app.utils.password_utils import hash_password, check_password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(24))
    last_name = db.Column(db.String(24))
    username = db.Column(db.String(24), index=True, unique=True)
    email = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(128))
    birth_date = db.Column(db.Date)
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def __repr__(self):
        return f'<User {self.username}>'