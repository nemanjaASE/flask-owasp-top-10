from app import create_app, login_manager
from app.services.exceptions import *
from flask import current_app, request

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    user_service = current_app.user_service
    try:
        return user_service.get_user(user_id)
    except InvalidInputException as e:
        current_app.logger.error('User Loader: %s', (str(e),))
    except EntityNotFoundError as e:
        excluded_endpoints = ['auth.login','main.info','auth.reset_request','auth.reset_password','auth.verify_otp', 'auth.logout']
        if request.endpoint and request.endpoint.startswith('static'):
            return
        if request.endpoint in excluded_endpoints:
            return
        current_app.entity_logger.log_entity_not_found(str(e))
    except DatabaseServiceError as e:
        current_app.security_logger.log_database_service_error(str(e))

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), port=9001)