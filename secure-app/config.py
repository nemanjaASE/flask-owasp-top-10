from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shared.env'))

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'instance/secure-app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL')
    DEBUG = os.getenv('DEBUG')
    MAIL_DEBUG = os.getenv('MAIL_DEBUG')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    RECAPTCHA_PUBLIC_KEY = os.getenv('SITE_KEY_RECAPTCHA')
    RECAPTCHA_PRIVATE_KEY = os.getenv('SECRET_KEY_RECAPTCHA')
    RECAPTCHA_V3_PRIVATE_KEY = os.getenv('SECRET_KEY_RECAPTCHA_V3')
    SESSION_COOKIE_HTTPONLY=os.getenv('SESSION_COOKIE_HTTPONLY')
    SESSION_COOKIE_SECURE=os.getenv('SESSION_COOKIE_SECURE')