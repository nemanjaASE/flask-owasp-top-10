from flask import render_template, redirect, url_for, current_app, flash
from flask_login import login_required, current_user

from app.forms.profile_form import ProfileForm
from app.forms.delete_user_form import DeleteUserForm

from app import requires_roles 

from app.dto.update_user_dto import UpdateUserDTO
from app.services.exceptions import *
from . import user_bp

@user_bp.route('/profile/<string:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    if user_id != current_user.id:
        return redirect(url_for('main.index'))

    user = current_app.user_service.get_user(user_id)
    form = ProfileForm(obj=user)
    
    form.current_username = user.username
    form.current_email = user.email

    if form.validate_on_submit():
        update_user_dto = UpdateUserDTO(
            user_id=user_id,
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            birth_date=form.birth_date.data
        )
        current_app.user_service.update_user(update_user_dto)
        current_app.security_logger.log_profile_change(user)
        return redirect(url_for('user.profile', user_id=user.id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)
    return render_template('profile.html', user=user, form=form)

@user_bp.route('/delete/<string:user_id>', methods=['POST'])
@login_required
@requires_roles('Admin')
def delete_user(user_id):
    form = DeleteUserForm()
    if form.validate_on_submit():
        current_app.user_service.delete_user(user_id)
        current_app.security_logger.log_delete_user(user_id, current_user.id)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)
    return redirect(url_for('main.dashboard'))

@user_bp.route('/request_author_role/<string:user_id>', methods=['GET'])
@login_required
@requires_roles('Reader')
def request_author_role(user_id):
    if user_id != current_user.id:
         return redirect(url_for('main.index'))

    if current_app.author_requests_service.check_existence(user_id):
        current_app.author_requests_service.create_author_request(user_id)
        current_app.security_logger.log_author_request(user_id)
        flash('You successfully send a request for an author role!', 'info')
    else:
        flash('Your request is still in progress.', 'info')
    return redirect(url_for('main.index'))