import redis

from datetime import timedelta
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from itsdangerous import URLSafeTimedSerializer
from .csp import csp

permissions_policy = {
        "geolocation": "'self'",
        "camera": "'none'",
        "microphone": "'none'",
        "fullscreen": "'self'",
    }   


def initialize_extensions(app):
    # Session
    app.permanent_session_lifetime = timedelta(minutes=30)
    # CSRF Protection
    CSRFProtect(app)
    # Flask-Mail
    mail = Mail(app)
    # Itsdangerous Serializer
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    # Limiter with Redis
    app.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    app.limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=app.config['REDIS_URL']
    )
    # Talisman
    Talisman(app, 
                        content_security_policy=csp, 
                        force_https=True, 
                        strict_transport_security=True,
                        x_content_type_options=True,
                        frame_options="DENY",
                        referrer_policy="strict-origin-when-cross-origin",
                        permissions_policy=permissions_policy,
                        session_cookie_secure=True,)
    
    return serializer, mail