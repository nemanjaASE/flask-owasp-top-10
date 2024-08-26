import unittest
from app.services.validators.login_user_validator import LoginUserValidator

class TestLoginUserValidator(unittest.TestCase):

    def test_validate_success(self):
        # Test validnih podataka
        data = {
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@'
        }
        self.assertIsNone(LoginUserValidator.validate(data))

    def test_validate_email_error(self):
        # Test praznog email-a
        data = {
            'email': '',
            'password': 'ValidPassword1@'
        }
        self.assertEqual(LoginUserValidator.validate(data), 'Email must not be empty and must be less than 32 characters long.')

        # Test predugog email-a
        data = {
            'email': 'a' * 33 + '@example.com',
            'password': 'ValidPassword1@'
        }
        self.assertEqual(LoginUserValidator.validate(data), 'Email must not be empty and must be less than 32 characters long.')

        # Test nevalidnog formata email-a
        data = {
            'email': 'invalid-email',
            'password': 'ValidPassword1@'
        }
        self.assertEqual(LoginUserValidator.validate(data), 'Invalid email format.')

    def test_validate_password_error(self):
        # Test prazne lozinke
        data = {
            'email': 'john.doe@example.com',
            'password': ''
        }
        self.assertEqual(LoginUserValidator.validate(data), 'Password must be between 8 and 64 characters long.')

        # Test kratke lozinke
        data = {
            'email': 'john.doe@example.com',
            'password': 'short'
        }
        self.assertEqual(LoginUserValidator.validate(data), 'Password must be between 8 and 64 characters long.')

        # Test preduge lozinke
        data = {
            'email': 'john.doe@example.com',
            'password': 'a' * 65
        }
        self.assertEqual(LoginUserValidator.validate(data), 'Password must be between 8 and 64 characters long.')

        # Test nevalidnih karaktera u lozinci
        data = {
            'email': 'john.doe@example.com',
            'password': 'Invalid#Pass'
        }
        self.assertEqual(LoginUserValidator.validate(data), 'Password can only contain letters, numbers, and special characters @$!%*?&.')

if __name__ == '__main__':
    unittest.main()