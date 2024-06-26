from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required

from app.forms.register_form import RegistrationForm
from app.forms.login_form import LoginForm
from app.forms.request_reset_form import RequestResetForm
from app.forms.reset_password_form import ResetPasswordForm

from app.dto.user_dto import UserRegistrationDTO
from app.dto.reset_password_dto import ResetPasswordDTO

from app.services.exceptions import *

from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    auth_service = current_app.auth_service
    pwned_service = current_app.pwned_service

    form = RegistrationForm(pwned_service)

    if form.validate_on_submit():
        user_dto = UserRegistrationDTO(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            birth_date=form.birth_date.data
        )
        
        try:
            auth_service.register(user_dto)
        except DuplicateEmailException as e:
            current_app.logger.error('User: %s', (str(e),))
        except InvalidPasswordException as e:
            current_app.logger.error('User password: %s', (str(e),))
        except DatabaseServiceError as e:
            current_app.logger.error('Database: %s', (str(e),))
        except Exception as e:
            current_app.logger.error('Unhandled: %s', (str(e),))
        
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    auth_service = current_app.auth_service
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            user = auth_service.authenticate(email, password)
            if user:
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Wrong email or password', 'error')
        except EntityNotFoundError as e:
            current_app.logger.error('User not found: %s', (str(e),))
            flash('Wrong email or password', 'error')
        except InvalidPasswordException as e:
            current_app.logger.error('User password: %s', (str(e),))
            flash('Wrong email or password', 'error')
        except DatabaseServiceError as e:
            current_app.logger.error('Database: %s', (str(e),))
        except Exception as e:
            current_app.logger.error('Unhandled: %s', (str(e),))

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    email_service = current_app.email_service
    form = RequestResetForm()

    if form.validate_on_submit():
        email = form.email.data

        try:
            email_service.send_reset_email(email)
        except EntityNotFoundError as e:
            current_app.logger.error('User not found: %s', (str(e),))
        except DatabaseServiceError as e:
            current_app.logger.error('Database: %s', (str(e),))
        except Exception as e:
            current_app.logger.error('Unhandled: %s', (str(e),))
        
        flash('If an account with that email address exists, you will receive an email with instructions to reset your password.', 'info')
        return redirect(url_for('main.info'))

    return render_template('reset_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    auth_service = current_app.auth_service
    pwned_service = current_app.pwned_service
    reset_token_service = current_app.reset_token_service

    form = ResetPasswordForm(pwned_service)

    try:
        reset_token_service.verify_token(token)

        if form.validate_on_submit():
            reset_password_dto = ResetPasswordDTO(password=form.password.data,token=token)

            updated_user = auth_service.reset_password(reset_password_dto)
    
            if updated_user:
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('auth.reset_request'))
    except ResetTokenException as e:
        current_app.logger.error('Reset token: %s', (str(e),))
        return redirect(url_for('auth.reset_request'))
    except EntityNotFoundError as e:
        current_app.logger.error('Reset Token not found: %s', (str(e),))
        return redirect(url_for('auth.reset_request'))
    except DatabaseServiceError as e:
        current_app.logger.error('Database: %s', (str(e),))
        return redirect(url_for('auth.reset_request'))
    except Exception as e:
        current_app.logger.error('Unhandled: %s', (str(e),))

    return render_template('reset_password.html', form=form)
    

