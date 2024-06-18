from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../common/statics')
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../common/templates')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)
    
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