import unittest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService
from app.services.exceptions import *
from app.dto.user_dto import UserRegistrationDTO
from app.dto.reset_password_dto import ResetPasswordDTO
from app.models import User
from datetime import datetime


class TestAuthService(unittest.TestCase):

    def setUp(self):
        # Mockovanje zavisnih servisa
        self.user_service = MagicMock()
        self.token_service = MagicMock()
        self.email_service = MagicMock()
        self.redis_client = MagicMock()

        # Kreiranje instance AuthService sa mockovanim servisima
        self.auth_service = AuthService(
            self.user_service, self.token_service, self.email_service, self.redis_client)

        # Kreiranje mock objekta korisnika
        self.user = User(id="123", email="test@example.com", password="12345678", is_verified=True)

    def test_authenticate_success(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.redis_client.get.return_value = None
        self.redis_client.delete.return_value = None

        with patch('app.utils.password_utils.check_password', return_value=True):
            authenticated_user = self.auth_service.authenticate("test@example.com", "12345678")
        
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.email, "test@example.com")

    def test_authenticate_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.auth_service.authenticate("", "")

    def test_authenticate_account_not_verified(self):
        self.user.is_verified = False
        self.user_service.get_user_by_email.return_value = self.user

        with self.assertRaises(AccountNotVerifiedError):
            self.auth_service.authenticate("test@example.com", "12345678")

    def test_authenticate_account_locked(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.redis_client.get.return_value = "locked"

        with self.assertRaises(AccountLockedException):
            self.auth_service.authenticate("test@example.com", "12345678")

    def test_authenticate_invalid_password_and_locked_account(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.redis_client.get.return_value = None

        self.redis_client.incr.side_effect = [1, 2, 3, 4, 5]

        with patch('app.utils.password_utils.check_password', return_value=False):
            for _ in range(4):
                with self.assertRaises(InvalidPasswordException):
                    self.auth_service.authenticate("test@example.com", "somepassword")
                    self.redis_client.incr.assert_called_with('failed_attempts:123')

            with self.assertRaises(AccountLockedException):
                self.auth_service.authenticate("test@example.com", "wrongpassword")
                self.redis_client.set.assert_called_once_with('lockout:123', 'locked', ex=15*60)
                self.assertEqual(self.redis_client.incr.call_count, 5)

    def test_register_success(self):
        user_dto = UserRegistrationDTO(
            email="new_user@example.com",
            password="ValidPass123",
            username="newuser",
            first_name="New",
            last_name="User",
            birth_date=datetime(1990, 1, 1).date()
        )

        self.user_service.create_user.return_value = self.user

        result = self.auth_service.register(user_dto)

        self.assertIsNotNone(result)
        self.assertEqual(result.email, "test@example.com")
        self.user_service.create_user.assert_called_with(user_dto)

    def test_register_invalid_input(self):
        user_dto = UserRegistrationDTO(
            email="",
            password="short",
            username="",
            first_name="",
            last_name="",
            birth_date=None
        )

        with self.assertRaises(InvalidInputException):
            self.auth_service.register(user_dto)

    def test_register_invalid_password_length(self):
        user_dto = UserRegistrationDTO(
            email="user@example.com",
            password="short",
            username="user",
            first_name="First",
            last_name="Last",
            birth_date=datetime(1990, 1, 1).date()
        )

        with self.assertRaises(InvalidInputException):
            self.auth_service.register(user_dto)
    
    def test_register_duplicate_email(self):
        user_dto = UserRegistrationDTO(
            email="existing_user@example.com",
            password="ValidPass123",
            username="existinguser",
            first_name="Existing",
            last_name="User",
            birth_date=datetime(1990, 1, 1).date()
        )

        self.user_service.create_user.side_effect = DuplicateEmailException()

        with self.assertRaises(DuplicateEmailException):
            self.auth_service.register(user_dto)

    def test_reset_password_success(self):
        reset_password_dto = ResetPasswordDTO(
            token="valid_token",
            password="NewValidPass123"
        )

        self.token_service.verify_reset_token.return_value = ("valid_token", "test@example.com")
        self.user_service.get_user_by_email.return_value = self.user
        self.user_service.update_password.return_value = self.user

        result = self.auth_service.reset_password(reset_password_dto)

        self.assertIsNotNone(result)
        self.assertEqual(result.email, "test@example.com")
        self.token_service.set_reset_used.assert_called_with("valid_token")
        self.user_service.update_password.assert_called_with("123", "NewValidPass123")
    
    def test_reset_password_invalid_input(self):
        reset_password_dto = ResetPasswordDTO(
            token="",
            password=""
        )

        with self.assertRaises(InvalidInputException):
            self.auth_service.reset_password(reset_password_dto)

    def test_reset_password_user_not_found(self):
        reset_password_dto = ResetPasswordDTO(
         token="valid_token",
            password="NewValidPass123"
        )

        self.token_service.verify_reset_token.return_value = ("valid_token", "nonexistent@example.com")
        self.user_service.get_user_by_email.side_effect = EntityNotFoundError('User', 'email', 'nonexistent@example.com')

        with self.assertRaises(EntityNotFoundError):
            self.auth_service.reset_password(reset_password_dto)