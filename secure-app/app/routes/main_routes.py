from flask import render_template, send_from_directory ,current_app, redirect, url_for
from flask_login import login_required, current_user
from app.forms.delete_user_form import DeleteUserForm
from app import requires_roles 

from . import main_bp


@main_bp.route('/')
@login_required
def index():
    posts = current_app.post_service.get_all_posts()
    return render_template('index.html',posts=posts)


@main_bp.route('/dashboard')
@login_required
@requires_roles('Admin')
def dashboard():
    form = DeleteUserForm()

    total_posts = 0
    total_users = 0
    users = []

    total_posts = current_app.post_service.post_count()
    total_users = current_app.user_service.user_count()
    users = current_app.user_service.get_all_users()
    requests = current_app.author_requests_service.get_all_author_requests()

    return render_template(
        'dashboard.html',  
        total_posts=total_posts,
        total_users=total_users,
        users=users,
        requests=requests,
        form=form)

@main_bp.route('/info')
def info():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('info.html')

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'img/favicon.ico')