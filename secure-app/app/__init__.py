from flask import Flask, flash, redirect, url_for
from datetime import timedelta
from flask_wtf import CSRFProtect
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from itsdangerous import URLSafeTimedSerializer
import os

from app.services import *
from app.repositories import *

from app.db import db

import logging
import redis

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

from functools import wraps

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def rate_limit_exceeded(e):
    flash('You have exceeded the request limit. Please try again later.', 'error')
    return redirect(url_for('main.info'))

def create_app():
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../common/statics')
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../common/templates')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object('config.Config')

    app.permanent_session_lifetime = timedelta(hours=1)
    db.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)
    mail = Mail(app)
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    # Initialize Limiter with Redis
    app.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    app.limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=app.config['REDIS_URL']
    )

    app.user_service = UserService(UserRepository())
    app.reset_token_service = ResetTokenService(ResetTokenRepository(), s)
    app.otp_token_service = OTPTokenService(s)
    app.email_service = EmailService(app.reset_token_service, app.user_service, mail, s)
    app.auth_service = AuthService(app.user_service, app.reset_token_service, app.email_service, app.redis_client)
    app.pwned_service = PwnedService()
    app.post_service = PostService(PostRepository())
    app.category_service = CategoryService(CategoryRepository())
    app.author_requests_service = AuthorRequestsService(AuthorRequestsRepository(), UserRepository())


    app.register_error_handler(429, rate_limit_exceeded)

    with app.app_context():
        from .routes.main_routes import main_bp
        from .routes.auth_routes import auth_bp
        from .routes.user_routes import user_bp
        from .routes.post_routes import post_bp

        app.register_blueprint(main_bp, url_prefix='/')
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(user_bp, url_prefix='/user')
        app.register_blueprint(post_bp, url_prefix='/post')

        from app.db_seed import seed_db
        db.drop_all();
        db.create_all()
        seed_db(db)
        print("Database seeded successfully.")
        
    return app