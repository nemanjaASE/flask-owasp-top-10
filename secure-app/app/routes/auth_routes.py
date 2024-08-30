from flask import render_template, redirect, url_for, flash, current_app, session, request
from flask_login import login_user, logout_user, login_required, current_user

from app.forms.register_form import RegistrationForm
from app.forms.login_form import LoginForm
from app.forms.request_reset_form import RequestResetForm
from app.forms.reset_password_form import ResetPasswordForm
from app.forms.otp_form import OTPForm

from app.services.exceptions import *
from app import requires_roles 

from . import auth_bp

from .helpers import auth_helpers

@auth_bp.route('/register', methods=['GET', 'POST'])
@current_app.limiter.limit("5 per hour")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm(current_app.pwned_service)

    if form.validate_on_submit():
        recaptcha_token = request.form.get('g-recaptcha-response')
        recaptcha_secret = current_app.config['RECAPTCHA_V3_PRIVATE_KEY']
        return auth_helpers.handle_register(recaptcha_token, recaptcha_secret, form)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@current_app.limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data    
        return auth_helpers.handle_authentication(email, password)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset_request', methods=['GET', 'POST'])
@current_app.limiter.limit("3 per minute; 10 per hour; 50 per day")
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetForm()

    if form.validate_on_submit():
        email = form.email.data
        return auth_helpers.handle_reset_request(email)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)
    return render_template('reset_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordForm(current_app.pwned_service)
    
    if form.validate_on_submit():
        return auth_helpers.handle_reset_password(token, form)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)
    return render_template('reset_password.html', form=form)

@auth_bp.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    return auth_helpers.handle_confirm_email(token)
        

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = OTPForm()
    if form.validate_on_submit():
        token = session.get('otp_token')

        if not token:
            flash('OTP token is missing or expired.', 'error')
            return redirect(url_for('main.info'))
        
        saved_otp, otp = auth_helpers.handle_verify_otp(form, token)
    
        if otp == saved_otp:
            user_id = session.get('user_id')
            user = current_app.user_service.get_user(user_id)
            if user:
                login_user(user)
                current_app.security_logger.log_successful_login_with_otp(user, 'email')
                session.pop('otp_token', None)
                session.pop('user_id', None)
                return redirect(url_for('main.index'))
            else:
                flash('Invalid OTP. Try again.', 'error')
        else:
            flash('Invalid OTP. Try again.', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)

    return render_template('verify_otp.html', form=form)

@auth_bp.route('/confirm_request', methods=['POST'])
@login_required
@requires_roles('Admin')
def confirm_request():
    request_id = request.form.get('request_id')
    status = request.form.get('status')
    return auth_helpers.handle_confirm_request(request_id, status, current_user.id)
