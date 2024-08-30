from flask import make_response, redirect, url_for, current_app, flash, abort, session, render_template
from flask_login import login_user

from app.services.exceptions import *

from app.dto.user_dto import UserRegistrationDTO
from app.dto.reset_password_dto import ResetPasswordDTO

from itsdangerous import SignatureExpired, BadSignature

def redirect_successfully(route_name, msg=None, flash_category=None):
    if msg is not None:
        flash(msg, flash_category)
    response = make_response(redirect(url_for(route_name)))
    response.status_code = 302
    return response

def handle_exception(exception, flash_category, route, status_code=None, msg=None, form=None):
    current_app.logger.error('Error: %s', str(exception))
    if msg:
        flash(msg, flash_category)

    if route:
        response = make_response(render_template(route, form=form))
        if status_code:
            response.status_code = status_code
        return response
    else:
        abort(status_code)

def handle_admin_login(email_service, user):
    otp_token, generated_time = email_service.send_otp(user.email)
    current_app.security_logger.log_otp_sent(user.email, 'email')
    session['otp_token'] = otp_token
    session['user_id'] = user.id
    session['otp_generated_time'] = generated_time
    return redirect_successfully('auth.verify_otp')

def handle_authentication(email, password):
    user = current_app.auth_service.authenticate(email, password)
    if user.role == 'Admin':
        return handle_admin_login(current_app.email_service, user)
    else:
        login_user(user)
        current_app.security_logger.log_successful_login(user)
    return redirect_successfully('main.index')

def handle_recaptcha_verify(recaptcha_secret, recaptcha_token):
    return current_app.recaptcha_service.verify_token(recaptcha_token, recaptcha_secret)
    
def handle_register(recaptcha_token, recaptcha_secret, form):
    if not handle_recaptcha_verify(recaptcha_secret, recaptcha_token):
        return render_template('register.html', form=form)
    
    user_dto = UserRegistrationDTO(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            birth_date=form.birth_date.data
        )
    
    current_app.auth_service.register(user_dto)
    current_app.security_logger.log_successful_registration(user_dto)
    current_app.email_service.send_confrimation_email(user_dto.email)
    current_app.security_logger.log_confirm_email_sent(user_dto.email)
    return redirect_successfully('main.info','Go to your email to verify your account.', 'info' )

def handle_reset_request(email):
    current_app.email_service.send_reset_email(email)
    current_app.security_logger.log_password_change_request(email)
    return redirect_successfully('main.info','If an account with that email address exists, you will receive an email with instructions to reset your password.', 'info' )

def handle_reset_password(token, form):
    if form.validate_on_submit():
        reset_password_dto = ResetPasswordDTO(password=form.password.data,token=token)
        updated_user = current_app.auth_service.reset_password(reset_password_dto)
        current_app.security_logger.log_successful_password_change(updated_user)
        return redirect_successfully('auth.login')


def handle_confirm_email(token):
    ret_token, ret_email = current_app.confirm_token_service.verify_confirm_token(token)
    current_app.security_logger.log_successful_email_confirm(ret_token, ret_email)
    flash('Your account has been successfully verified. You can now log in.', 'info')
    return redirect(url_for('main.info'))
   
def handle_verify_otp(form, token):
    otp = (
            form.otp_1.data +
            form.otp_2.data +
            form.otp_3.data +
            form.otp_4.data +
            form.otp_5.data +
            form.otp_6.data
        )

    saved_otp = current_app.otp_token_service.verify_otp_token(token)

    if saved_otp is None:
        return redirect_successfully('main.info', 'The OTP is either invalid or expired.', 'error')
    return saved_otp, otp
    
def handle_confirm_request(request_id, status, admin_id):
    user = current_app.author_requests_service.update_author_request(request_id, status)
    current_app.security_logger.log_author_request_accepted(user.id, admin_id)
    return redirect_successfully('main.dashboard')