from app import db
from app.models.user import User

def get_all_users():
    return User.query.all()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def add_user(new_user):
    db.session.add(new_user)
    db.session.commit()

def update_user(user, username, first_name, last_name, email, birth_date):
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.birth_date = birth_date
    db.session.commit()

def delete_user(user):
    db.session.delete(user)
    db.session.commit()

def user_count():
    return User.query.count()

def is_username_unique(username):
    return User.query.filter_by(username=username).first() is None;

def is_email_unique(email):
    return User.query.filter_by(email=email).first() is None;