from app.services import *
from app.repositories import *

def register_services(app, s, mail):
    app.user_service = UserService(UserRepository())
    app.reset_token_service = ResetTokenService(ResetTokenRepository(), s)
    app.confirm_token_service = ConfirmTokenService(ConfirmTokenRepository(), app.user_service, s)
    app.otp_token_service = OTPTokenService(s)
    app.email_service = EmailService(app.reset_token_service, app.confirm_token_service, app.user_service, mail, s)
    app.auth_service = AuthService(app.user_service, app.reset_token_service, app.email_service, app.redis_client)
    app.pwned_service = PwnedService()
    app.post_service = PostService(PostRepository())
    app.category_service = CategoryService(CategoryRepository())
    app.author_requests_service = AuthorRequestsService(AuthorRequestsRepository(), UserRepository())
    app.recaptcha_service = RecaptchaService()