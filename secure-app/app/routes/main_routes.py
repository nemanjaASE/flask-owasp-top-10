from flask import render_template, current_app
from flask_login import login_required
from app.forms.delete_user_form import DeleteUserForm
from app import requires_roles 

from app.services.exceptions.database_service_error import DatabaseServiceError

from . import main_bp


@main_bp.route('/')
@login_required
def index():
    post_service = current_app.post_service
    posts = []
    try:
        posts = post_service.get_all_posts()
    except DatabaseServiceError as e:
        current_app.logger.error('Database: %s', (str(e),))
    except Exception as e:
        current_app.logger.error('Unhandled: %s', (str(e),))

    return render_template('index.html',posts=posts)


@main_bp.route('/dashboard')
@login_required
@requires_roles('Admin')
def dashboard():
    form = DeleteUserForm()
    post_service = current_app.post_service
    user_service = current_app.user_service
    author_requests_service = current_app.author_requests_service

    total_posts = 0
    total_users = 0
    users = []
    try:
         total_posts = post_service.post_count()
         total_users = user_service.user_count()
         users = user_service.get_all_users()
         requests = author_requests_service.get_all_author_requests()
        
    except DatabaseServiceError as e:
        current_app.logger.error('Database: %s', (str(e),))
    except Exception as e:
        current_app.logger.error('Unhandled: %s', (str(e),))


    return render_template(
        'dashboard.html',  
        total_posts=total_posts,
        total_users=total_users,
        users=users,
        requests=requests,
        form=form)

@main_bp.route('/info')
def info():
    return render_template('info.html')