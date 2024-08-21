from app import create_app, login_manager
from app.services.exceptions import *
from flask import current_app, g

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    user_service = current_app.user_service

    try:
        return user_service.get_user(user_id)
    except InvalidParameterException as e:
        current_app.logger.error('User Loader: %s', (str(e),))
    except EntityNotFoundError as e:
        current_app.logger.error('User Loader: %s', (str(e),))
    except DatabaseServiceError as e:
        current_app.logger.error('User Loader: %s', (str(e),))
    except Exception as e:
        current_app.logger.error('Unhandled: %s', (str(e),))

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), port=9001)