from flask import render_template, redirect, url_for, flash, current_app, session, request
from flask_login import login_user, logout_user, login_required

from app.forms.register_form import RegistrationForm
from app.forms.login_form import LoginForm
from app.forms.request_reset_form import RequestResetForm
from app.forms.reset_password_form import ResetPasswordForm
from app.forms.otp_form import OTPForm

from app.services.exceptions import *

from . import auth_bp

from .helpers import auth_helpers

@auth_bp.route('/register', methods=['GET', 'POST'])
@current_app.limiter.limit("5 per hour")
def register():
    pwned_service = current_app.pwned_service
    form = RegistrationForm(pwned_service)

    if form.validate_on_submit():
        recaptcha_token = request.form.get('g-recaptcha-response')
        recaptcha_secret = current_app.config['RECAPTCHA_V3_PRIVATE_KEY']
        return auth_helpers.handle_register(recaptcha_token, recaptcha_secret, form)

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@current_app.limiter.limit("10 per minute")
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data    
        return auth_helpers.handle_authentication(email, password, form)
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset_request', methods=['GET', 'POST'])
@current_app.limiter.limit("3 per minute; 10 per hour; 50 per day")
def reset_request():
    form = RequestResetForm()

    if form.validate_on_submit():
        email = form.email.data
        return auth_helpers.handle_reset_request(email)

    return render_template('reset_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    pwned_service = current_app.pwned_service
    form = ResetPasswordForm(pwned_service)
    
    if form.validate_on_submit():
        return auth_helpers.handle_reset_password(token, form)
    
    return render_template('reset_password.html', form=form)

@auth_bp.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    return auth_helpers.handle_confirm_email(token)
        

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    user_service = current_app.user_service

    form = OTPForm()
    if form.validate_on_submit():
        token = session.get('otp_token')

        if not token:
            flash('OTP token is missing or expired.', 'error')
            return redirect(url_for('main.info'))
        
        saved_otp, otp = auth_helpers.handle_verify_otp(form, token)
    
        if otp == saved_otp:
            user_id = session.get('user_id')
            user = user_service.get_user(user_id)
            if user:
                login_user(user)
                session.pop('otp_token', None)
                session.pop('user_id', None)
                return redirect(url_for('main.index'))
            else:
                flash('Invalid OTP. Try again.', 'error')
        else:
            flash('Invalid OTP. Try again.', 'error')

    return render_template('verify_otp.html', form=form)

@auth_bp.route('/confirm_request', methods=['GET', 'POST'])
def confirm_request():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        status = request.form.get('status')
        return auth_helpers.handle_confirm_request(request_id, status)

    return redirect(url_for('main.dashboard'))
