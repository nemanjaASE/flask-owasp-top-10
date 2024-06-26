from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
user_bp = Blueprint('user', __name__)
post_bp = Blueprint('post', __name__)
main_bp = Blueprint('main', __name__)

__all__ = ["auth_bp",
           "user_bp",
           "post_bp",
           "main_bp"]

