import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from flask import request

class SecurityLogger:
    def __init__(self, app=None, log_file='security.log', max_bytes=1024*1024, backup_count=5):
        self.logger = logging.getLogger('security')
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)

    def log_successful_login(self, user):
        self.logger.info(
            f"User {user.email} (ID: {user.id}) successfully logged in at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}. Session ID: {request.cookies.get('session')}."
        )

    def log_failed_login(self, user_email, error_message):
        self.logger.warning(
            f"Failed login attempt for user {user_email} at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}. Reason: {error_message}"
        )
    
    def log_invalid_input(self, field_name, error_message):
        self.logger.warning(
            f"Invalid input detected for field '{field_name}' at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}. Reason: {error_message}"
        )
    
    def log_successful_registration(self, user):
        self.logger.info(
            f"User {user.email} (username: {user.username}) successfully registered at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}."
        )
    
    def log_failed_registration(self, email, errors):
        self.logger.warning(
            f"Failed registration attempt for email '{email}' at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}. Reason: {errors}"
        )
    def log_unauthorised_request(self):
        self.logger.warning(
            f"Unauthenticated request from IP {request.remote_addr} "
            f"attempted to access {request.endpoint} using {request.headers.get('User-Agent')} "
            f"at {request.url}."
        )

    def log_access_denied(self, user):
        self.logger.warning(
            f"Access denied for user {user.email} (ID: {user.id}) at {datetime.now().isoformat()} "
            f"while trying to access route '{request.endpoint}' from IP {request.remote_addr} using {request.headers.get('User-Agent')}."
        )
    
    def log_otp_sent(self, admin_email, otp_method):
        self.logger.info(
            f"OTP sent to admin {admin_email} via {otp_method} at {datetime.now().isoformat()}. "
            f"IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}."
        )

    def log_successful_login_with_otp(self, user, otp_method):
        self.logger.info(
            f"User {user.email} (ID: {user.id}) successfully logged in with OTP at {datetime.now().isoformat()}. "
            f"OTP Method: {otp_method}. IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}. "
            f"Session ID: {request.cookies.get('session')}."
        )

    def log_database_service_error(self, error_message):
        self.logger.error(
            f"Database Service Error at {datetime.now().isoformat()}: {error_message}. "
            f"IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}."
        )

    def log_unhandled_exception(self, exception):
        self.logger.error(
            f"Unhandled Exception at {datetime.now().isoformat()}: {str(exception)}. "
            f"IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}. "
            f"URL: {request.url}. Endpoint: {request.endpoint}"
        )
    
    def log_password_change_request(self, email):
        self.logger.info(
            f"Password change request initiated by user {email} at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}."
        )

    def log_successful_password_change(self, user):
        self.logger.info(
            f"Password successfully changed for user {user.email} (ID: {user.id}) at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}."
        )

    def log_token_exception(self, user_id, msg):
         self.logger.warning(
            f"Invalid reset token request from user (ID: {user_id}) at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}. Reason: {msg}"
        )
    
    def log_successful_email_confirm(self, token, email):
        self.logger.info(
            f"User {email} (ID: {token.user_id}) successfully confirm email at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}."
        )

    def log_successful_email_confirm(self, token, email):
        self.logger.info(
            f"User {email} (ID: {token.user_id}) successfully confirmed email at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}."
        )

    def log_confirm_email_sent(self, user_email):
        self.logger.info(
            f"Confirmation email sent to {user_email} at {datetime.now().isoformat()}. "
            f"IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}."
        )

    def log_signature_expired(self, msg):
        self.logger.warning(
            f"{msg}. "
            f"IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}."
        )

    def log_bad_signature(self, msg):
        self.logger.warning(
            f"{msg}. "
            f"IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}."
        )

    def log_profile_change(self, user):
        self.logger.info(
            f"Profile updated for user {user.email} (ID: {user.id}) at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}.")
    
    def log_delete_user(self, user_id, admin_id):
        self.logger.info(
            f"User account with ID {user_id} has been deleted by admin with ID {admin_id} at {datetime.now().isoformat()} "
            f"from IP {request.remote_addr} using {request.headers.get('User-Agent')}."
        )
    
    def log_author_request(self, user_id):
        self.logger.info(
            f"User with ID {user_id} has initiated a request for the AUTHOR role at {datetime.now().isoformat()}. "
            f"IP address {request.remote_addr} using User-Agent: {request.headers.get('User-Agent')}."
        )
    
    def log_author_request_accepted(self, user_id, admin_id):
        self.logger.info(
            f"Admin with ID {admin_id} has approved the AUTHOR role request for user with ID {user_id} "
            f"at {datetime.now().isoformat()}. IP Address: {request.remote_addr}. User-Agent: {request.headers.get('User-Agent')}."
        )