from flask import render_template, redirect, url_for, flash, current_app, session, request
from flask_login import login_user, logout_user, login_required

from app.forms.register_form import RegistrationForm
from app.forms.login_form import LoginForm
from app.forms.request_reset_form import RequestResetForm
from app.forms.reset_password_form import ResetPasswordForm
from app.forms.otp_form import OTPForm

from app.dto.user_dto import UserRegistrationDTO
from app.dto.reset_password_dto import ResetPasswordDTO

from app.services.exceptions import *

from . import auth_bp

from itsdangerous import SignatureExpired, BadSignature

@auth_bp.route('/register', methods=['GET', 'POST'])
@current_app.limiter.limit("5 per hour")
def register():
    auth_service = current_app.auth_service
    pwned_service = current_app.pwned_service
    email_service = current_app.email_service
    recaptcha_service = current_app.recaptcha_service

    form = RegistrationForm(pwned_service)

    if form.validate_on_submit():

        recaptcha_token = request.form.get('g-recaptcha-response')
        recaptcha_secret = current_app.config['RECAPTCHA_V3_PRIVATE_KEY']

        if not recaptcha_service.verify_token(recaptcha_token, recaptcha_secret):
            render_template('register.html', form=form)

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
            current_app.logger.error('User: %s', (str(e),))
        except InvalidPasswordException as e:
            current_app.logger.error('User password: %s', (str(e),))
        except DatabaseServiceError as e:
            current_app.logger.error('Database: %s', (str(e),))
        except Exception as e:
            current_app.logger.error('Unhandled: %s', (str(e),))
        flash('Go to your email to verify your account.', 'info')
        return redirect(url_for('main.info'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@current_app.limiter.limit("10 per minute")
def login():
    auth_service = current_app.auth_service
    email_service = current_app.email_service

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            user = auth_service.authenticate(email, password)
            if user:
                if user.role == 'Admin':
                    otp_token, generated_time = email_service.send_otp(user.email)
                    session['otp_token'] = otp_token
                    session['user_id'] = user.id
                    session['otp_generated_time'] = generated_time
                    return redirect(url_for('auth.verify_otp'))
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Wrong email or password', 'error')
        except AccountNotVerifiedError as e:
            current_app.logger.error('User account not verified: %s', (str(e),))
            flash(str(e), 'info')
            return redirect(url_for('main.info'))
        except EntityNotFoundError as e:
            current_app.logger.error('User not found: %s', (str(e),))
            flash('Wrong email or password', 'error')
        except InvalidPasswordException as e:
            current_app.logger.error('User password: %s', (str(e),))
            flash('Wrong email or password', 'error')
        except AccountLockedException as e:
            current_app.logger.error('Account Locked: %s', (str(e),))
            flash(str(e), 'error')
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
@current_app.limiter.limit("3 per minute; 10 per hour; 50 per day")
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
    token_service = current_app.token_service

    form = ResetPasswordForm(pwned_service)

    try:
        token_service.verify_reset_token(token)

        if form.validate_on_submit():
            reset_password_dto = ResetPasswordDTO(password=form.password.data,token=token)

            updated_user = auth_service.reset_password(reset_password_dto)
    
            if updated_user:
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('auth.reset_request'))
    except TokenException as e:
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

@auth_bp.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    token_service = current_app.token_service

    try:
        token_service.verify_confirm_token(token)
    except TokenException as e:
        current_app.logger.error('Confirm token: %s', (str(e),))
        return redirect(url_for('auth.login'))
    except EntityNotFoundError as e:
        current_app.logger.error('Confirm Token not found: %s', (str(e),))
        return redirect(url_for('auth.login'))
    except DatabaseServiceError as e:
        current_app.logger.error('Database: %s', (str(e),))
        return redirect(url_for('auth.login'))
    except Exception as e:
        current_app.logger.error('Unhandled: %s', (str(e),))

    flash('Your account has been successfully verified. You can now log in.', 'info')

    return redirect(url_for('main.info'))
        

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    user_service = current_app.user_service
    otp_token_service = current_app.otp_token_service

    form = OTPForm()
    if form.validate_on_submit():
        otp = (
            form.otp_1.data +
            form.otp_2.data +
            form.otp_3.data +
            form.otp_4.data +
            form.otp_5.data +
            form.otp_6.data
        )
        token = session.get('otp_token')

        if not token:
            flash('OTP token is missing or expired.', 'error')
            return redirect(url_for('main.info'))

        try:
            saved_otp = otp_token_service.verify_otp_token(token)
        except SignatureExpired as e:
            current_app.logger.error('OTP: %s', (str(e),))
            flash('The OTP has expired.', 'info')
            return redirect(url_for('main.info'))
        except BadSignature as e:
            current_app.logger.error('OTP: %s', (str(e),))
            flash('The OTP is invalid.', 'info')
            return redirect(url_for('main.info'))
        except Exception as e:
            current_app.logger.error('Error: %s', (str(e),))
            return redirect(url_for('auth.login'))
        

        if saved_otp is None:
            flash('The OTP is either invalid or expired.', 'error')
            return redirect(url_for('main.info'))
    
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
    author_requests_service = current_app.author_requests_service

    if request.method == 'POST':
        request_id = request.form.get('request_id')
        status = request.form.get('status')

        author_requests_service.update_request(request_id, status)

    return redirect(url_for('main.dashboard'))
