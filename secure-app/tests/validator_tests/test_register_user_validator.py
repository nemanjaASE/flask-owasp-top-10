import unittest
from datetime import date
from app.services.validators.register_user_validator import RegisterUserValidator

class TestRegisterUserValidator(unittest.TestCase):

    def test_validate_success(self):
        # Test validnih podataka
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertIsNone(RegisterUserValidator.validate(data))

    def test_validate_first_name_error(self):
        # Test praznog prvog imena
        data = {
            'first_name': '',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'First name cannot be empty.')

        # Test predugog prvog imena
        data = {
            'first_name': 'a' * 25,
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'First name must be 24 characters or less.')

    def test_validate_last_name_error(self):
        # Test praznog prezimena
        data = {
            'first_name': 'John',
            'last_name': '',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Last name cannot be empty.')

        # Test predugog prezimena
        data = {
            'first_name': 'John',
            'last_name': 'a' * 25,
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Last name must be 24 characters or less.')

    def test_validate_username_error(self):
        # Test praznog korisničkog imena
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': '',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Username cannot be empty.')

        # Test predugog korisničkog imena
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'a' * 25,
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Username must be 24 characters or less.')

        # Test nevalidnog korisničkog imena
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'invalid username',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Username can only contain letters, numbers, and underscores.')

    def test_validate_email_error(self):
        # Test praznog email-a
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': '',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Email must not be empty and must be less than 32 characters long.')

        # Test predugog email-a
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'a' * 33 + '@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Email must not be empty and must be less than 32 characters long.')

        # Test nevalidnog formata email-a
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'invalid-email',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Invalid email format.')

    def test_validate_password_error(self):
        # Test kratke lozinke
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'short',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Password must be between 8 and 64 characters long.')

        # Test duge lozinke
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'a' * 65,
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Password must be between 8 and 64 characters long.')

        # Test nevalidnih karaktera u lozinci
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'Invalid#Pass',
            'birth_date': date(1900,1,1)
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Password can only contain letters, numbers, and special characters @$!%*?&.')

    def test_validate_birth_date_error(self):
        # Test praznog datuma rođenja
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': ''
        }
        self.assertEqual(RegisterUserValidator.validate(data), 'Birth cannot be empty.')

        # Test validnog formata datuma
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@example.com',
            'password': 'ValidPassword1@',
            'birth_date': date(1900,1,1,)
        }
        self.assertEqual(RegisterUserValidator.validate(data), None)

if __name__ == '__main__':
    unittest.main()