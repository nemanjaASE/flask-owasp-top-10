from flask import render_template
from flask_login import login_required
from app.services import user_service, post_service
from app.forms.delete_user_form import DeleteUserForm

from . import main_bp


@main_bp.route('/')
@login_required
def index():
    posts = post_service.get_all_posts();
    return render_template('index.html',posts=posts)

@main_bp.route('/dashboard')
def dashboard():
    form = DeleteUserForm()
    total_posts = post_service.posts_count()
    total_users = user_service.user_count()
    users = user_service.get_all_users()

    return render_template(
        'dashboard.html',  
        total_posts=total_posts,
        total_users=total_users,
        users=users,
        form=form)