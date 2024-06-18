from flask import render_template, redirect, url_for
from flask_login import login_required
from app.services import user_service
from app.forms.profile_form import ProfileForm
from app.forms.delete_user_form import DeleteUserForm

from . import user_bp

@user_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user = user_service.get_user_by_id(user_id)
    form = ProfileForm(obj=user)
    
    form.current_username = user.username
    form.current_email = user.email

    if form.validate_on_submit():
        user_service.update_user(
            user,
            form.username.data,
            form.first_name.data,
            form.last_name.data,
            form.email.data,
            form.birth_date.data
        )

        return redirect(url_for('user.profile', user_id=user.id))

    return render_template('profile.html', user=user, form=form)

@user_bp.route('/users')
@login_required
def users():
    users = user_service.get_all_users()
    return render_template('users.html', users=users)

@user_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    form = DeleteUserForm()
    if form.validate_on_submit():
        user = user_service.get_user_by_id(user_id)
        user_service.delete_user(user)
    return redirect(url_for('main.dashboard'))