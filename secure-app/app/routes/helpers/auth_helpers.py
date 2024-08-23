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
    session['otp_token'] = otp_token
    session['user_id'] = user.id
    session['otp_generated_time'] = generated_time
    return redirect_successfully('auth.verify_otp')

def handle_authentication(email, password, form):
    auth_service = current_app.auth_service
    email_service = current_app.email_service

    try:
        user = auth_service.authenticate(email, password)
        if user.role == 'Admin':
            return handle_admin_login(email_service, user)
        else:
            login_user(user)
            return redirect_successfully('main.index')
    except AccountNotVerifiedError as e:
        return redirect_successfully('main.info', str(e), 'info')
    except (EntityNotFoundError, InvalidPasswordException) as e:
        return handle_exception(e, 'error', 'login.html', 400, 'Wrong email or password', form)
    except AccountLockedException as e:
        return handle_exception(e, 'error', 'login.html', 401, str(e), form)
    except DatabaseServiceError as e:
        return handle_exception(e, 'error', None, 500)
    except Exception as e:
        return handle_exception(e, 'error', None, 500)

def handle_recaptcha_verify(recaptcha_secret, recaptcha_token):
    recaptcha_service = current_app.recaptcha_service
    return recaptcha_service.verify_token(recaptcha_token, recaptcha_secret)
    
def handle_register(recaptcha_token, recaptcha_secret, form):
    auth_service = current_app.auth_service
    email_service = current_app.email_service
    
    if not handle_recaptcha_verify(recaptcha_secret, recaptcha_token):
        return render_template('register.html', form=form)
    
    user_dto = UserRegistrationDTO(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            birth_date=form.birth_date.data,
            role='Reader'
        )
    
    try:
        auth_service.register(user_dto)
        email_service.send_confrimation_email(user_dto.email)
    except DuplicateEmailException as e:
        return handle_exception(e, 'error', 'register.html', status_code=409, form=form)
    except InvalidPasswordException as e:
        return handle_exception(e, 'error', 'register.html', 400, 'Password does not meet the requirements.', form)
    except DatabaseServiceError as e:
        return handle_exception(e, 'error', 'register.html', status_code=500, form=form)
    except Exception as e:
        return handle_exception(e, 'error', 'register.html', status_code=500, form=form)
    
    return redirect_successfully('main.info','Go to your email to verify your account.', 'info' )

def handle_reset_request(email):
    email_service = current_app.email_service
    
    try:
        email_service.send_reset_email(email)
        return redirect_successfully('main.info','If an account with that email address exists, you will receive an email with instructions to reset your password.', 'info' )
    except EntityNotFoundError as e:
        return redirect_successfully('main.info','If an account with that email address exists, you will receive an email with instructions to reset your password.', 'info' )
    except DatabaseServiceError as e:
        return handle_exception(e, 'error', 'register.html', status_code=500)
    except Exception as e:
        return handle_exception(e, 'error', 'register.html', status_code=500)

def handle_reset_password(token, form):
    token_service = current_app.token_service
    auth_service = current_app.auth_service

    try:
        token_service.verify_reset_token(token)

        if form.validate_on_submit():
            reset_password_dto = ResetPasswordDTO(password=form.password.data,token=token)

            updated_user = auth_service.reset_password(reset_password_dto)
    
            if updated_user:
                return redirect_successfully('auth.login')
            else:
                return redirect_successfully('auth.reset_request')

    except TokenException as e:
       return redirect_successfully('auth.reset_request')
    except EntityNotFoundError as e:
        return redirect_successfully('auth.reset_request')
    except DatabaseServiceError as e:
        return handle_exception(e, 'error', 'reset_request.html', status_code=500)
    except Exception as e:
        return handle_exception(e, 'error', 'reset_request.html', status_code=500)

    return render_template('reset_password.html', form=form)

def handle_confirm_email(token):
    token_service = current_app.token_service

    try:
        token_service.verify_confirm_token(token)

        flash('Your account has been successfully verified. You can now log in.', 'info')
        return redirect(url_for('main.info'))
    except (TokenException, EntityNotFoundError) as e:
        return redirect_successfully('auth.login')
    except DatabaseServiceError as e:
         return handle_exception(e, 'error', 'login.html', status_code=500)
    except Exception as e:
        return handle_exception(e, 'error', 'login.html', status_code=500)

def handle_verify_otp(form, token):
    user_service = current_app.user_service
    otp_token_service = current_app.otp_token_service

    otp = (
            form.otp_1.data +
            form.otp_2.data +
            form.otp_3.data +
            form.otp_4.data +
            form.otp_5.data +
            form.otp_6.data
        )

    try:
        saved_otp = otp_token_service.verify_otp_token(token)

        if saved_otp is None:
            return redirect_successfully('main.info', 'The OTP is either invalid or expired.', 'error')

        return saved_otp, otp
    except SignatureExpired as e:
        return redirect_successfully('main.info', 'The OTP has expired.', 'error')
    except BadSignature as e:
        return redirect_successfully('main.info', 'The OTP is invalid.', 'error')
    except Exception as e:
        return handle_exception(e, 'error', 'verify_otp.html', status_code=500)
    
def handle_confirm_request(request_id, status):
    author_requests_service = current_app.author_requests_service
    try:
        author_requests_service.update_request(request_id, status)
        return redirect_successfully(url_for('main.dashboard'))
    except (InvalidParameterException, EntityNotFoundError) as e:
         return handle_exception(e, 'error', 'dashboard.html', 400)
    except DatabaseServiceError as e:
         return handle_exception(e, 'error', 'dashboard.html', status_code=500)
    except Exception as e:
        return handle_exception(e, 'error', 'dashboard.html', status_code=500)