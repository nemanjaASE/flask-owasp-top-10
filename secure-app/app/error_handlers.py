from flask import render_template, current_app, redirect, url_for, flash, request, make_response, abort
from flask_login import current_user
from app.services.exceptions import *
from app.forms.login_form import LoginForm
from app.forms.register_form import RegistrationForm
from app.forms.post_form import PostForm

def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_error(error):
        if current_user.is_authenticated:
            if hasattr(app, 'security_logger'):
                app.security_logger.log_access_denied(current_user)
        return render_template('403.html'), 403

    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        current_app.security_logger.log_unhandled_exception(e)
        return render_template('500.html', error=str(e)), 500
    
    @app.errorhandler(404)
    def handle_unhandled_exception(e):
        current_app.security_logger.log_unhandled_exception(e)
        return render_template('404.html', error=str(e)), 404

    @app.errorhandler(AccountNotVerifiedError)
    def handle_account_not_verified_exception(e):
        current_app.security_logger.log_failed_login(e.email, str(e))
        flash(str(e), 'info')
        return redirect(url_for('main.info'))
    
    @app.errorhandler(TokenExpiredException)
    def handle_signature_expired_exception(e):
        current_app.security_logger.log_signature_expired(str(e))
        return redirect_successfully('main.info', 'The OTP has expired.', 'error')
    
    @app.errorhandler(TokenBadSignatureException)
    def handle_bad_signature_exception(e):
        current_app.security_logger.log_bad_signature(str(e))
        return redirect_successfully('main.info', 'The OTP is invalid.', 'error')

    @app.errorhandler(EntityNotFoundError)
    def handle_entity_not_found(e):
        if request.endpoint == 'auth.login':
            form = LoginForm()
            current_app.security_logger.log_failed_login(e.field_value, str(e))
            return handle_exception(e, 'error', 'login.html', status_code=400, msg='Wrong email or password', form=form)
        elif request.endpoint == 'auth.reset_request':
            current_app.entity_logger.log_entity_not_found(str(e))
            return redirect_successfully('main.info','If an account with that email address exists, you will receive an email with instructions to reset your password.', 'info' )
        elif request.endpoint == 'auth.reset_password':
            current_app.entity_logger.log_entity_not_found(str(e))
            return redirect_successfully('auth.reset_request')
        elif request.endpoint == 'auth.confirm_email':
            current_app.entity_logger.log_entity_not_found(str(e))
            return redirect_successfully('auth.login')
        elif request.endpoint == 'auth.confirm_request':
            current_app.entity_logger.log_entity_not_found(str(e))
            return handle_exception(e, 'error', 'dashboard.html', 400)
        elif request.endpoint == 'post.add_post':
            form = PostForm()
            current_app.entity_logger.log_entity_not_found(str(e))
            return render_template('add_post.html', form=form)
        else:
            current_app.entity_logger.log_entity_not_found(str(e))
            return redirect(url_for('main.index'))  
    
    @app.errorhandler(InvalidInputException)
    def handle_invalid_input(e):
        current_app.security_logger.log_failed_login(e.parameter_name, str(e))
        if request.endpoint == 'auth.login':
            form = LoginForm(request.form)  
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        current_app.security_logger.log_failed_login(field, error)
            return handle_exception(e, 'error', 'login.html', 400, 'Wrong email or password', form)
        else:
            pass

    @app.errorhandler(InvalidPasswordException)
    def handle_wrong_password(e):
        current_app.security_logger.log_failed_login(e.email, str(e))
        form = LoginForm()
        return handle_exception(e, 'error', 'login.html', 400, 'Wrong email or password', form)
    
    @app.errorhandler(AccountLockedException)
    def handle_account_locked(e):
        current_app.security_logger.log_failed_login(e.email, str(e))
        form = LoginForm()
        return handle_exception(e, 'error', 'login.html', 401, str(e), form)
    
    @app.errorhandler(DatabaseServiceError)
    def handle_database_error(e):
        current_app.security_logger.log_database_service_error(str(e))
        return handle_exception(e, 'error', None, 500)
    
    @app.errorhandler(EmailAlreadyExistsException)
    def handle_duplicate_email(e):
        current_app.security_logger.log_failed_registration(e.email, str(e))
        form = RegistrationForm(current_app.pwned_service)
        return handle_exception(e, 'error', 'register.html', status_code=409, form=form, 
                                msg='The provided credentials are already in use. Please choose a different username or email')
    
    @app.errorhandler(UsernameAlreadyExistsException)
    def handle_duplicate_username(e):
        current_app.security_logger.log_failed_registration(e.username, str(e))
        form = RegistrationForm(current_app.pwned_service)
        return handle_exception(e, 'error', 'register.html', status_code=409, form=form, 
                                msg='The provided credentials are already in use. Please choose a different username or email')

    @app.errorhandler(TokenException)
    def handle_token_exception(e):
        if request.endpoint == 'auth.reset_password':
            current_app.security_logger.log_token_exception(e.user_id, e.message)
            return redirect_successfully('auth.reset_request')
        else:
            pass
    
    @app.errorhandler(429)
    def handle_limit_exceeded(e):
        return redirect_successfully('main.info', 'You have exceeded the request limit. Please try again later.', 'info')

    @app.before_request
    def log_unauthenticated_request():
        if not current_user.is_authenticated:
            excluded_endpoints = [
                'auth.login',
                'main.info',
                'auth.reset_request',
                'auth.reset_password',
                'auth.verify_otp',
                'auth.logout',
                'auth.register'
            ]
            if request.endpoint and request.endpoint.startswith('static'):
                return
            if request.endpoint in excluded_endpoints:
                return
            current_app.security_logger.log_unauthorised_request()

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

    def redirect_successfully(route_name, msg=None, flash_category=None):
        if msg is not None:
            flash(msg, flash_category)
        response = make_response(redirect(url_for(route_name)))
        response.status_code = 302
        return response