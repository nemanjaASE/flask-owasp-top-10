import unittest
import re
from datetime import date
from app.services.validators.base_user_validator import BaseUserValidator

class TestBaseUserValidator(unittest.TestCase):

    def test_validate_email(self):
        # Test validan email
        self.assertIsNone(BaseUserValidator.validate_email('test@example.com'))
        # Test praznog email-a
        self.assertEqual(BaseUserValidator.validate_email(''), 'Email must not be empty and must be less than 32 characters long.')
        # Test email-a koji je predug
        self.assertEqual(BaseUserValidator.validate_email('a' * 33 + '@example.com'), 'Email must not be empty and must be less than 32 characters long.')
        # Test nevalidan format email-a
        self.assertEqual(BaseUserValidator.validate_email('invalid-email'), 'Invalid email format.')

    def test_validate_password(self):
        # Test validna lozinka
        self.assertIsNone(BaseUserValidator.validate_password('ValidPass1@'))
        # Test kratke lozinke
        self.assertEqual(BaseUserValidator.validate_password('short'), 'Password must be between 8 and 64 characters long.')
        # Test duge lozinke
        self.assertEqual(BaseUserValidator.validate_password('a' * 65), 'Password must be between 8 and 64 characters long.')
        # Test lozinke sa nevalidnim karakterima
        self.assertEqual(BaseUserValidator.validate_password('Invalid#Pass'), 'Password can only contain letters, numbers, and special characters @$!%*?&.')

    def test_validate_first_name(self):
        # Test validno ime
        self.assertIsNone(BaseUserValidator.validate_first_name('John'))
        # Test prazno ime
        self.assertEqual(BaseUserValidator.validate_first_name(''), 'First name cannot be empty.')
        # Test predugo ime
        self.assertEqual(BaseUserValidator.validate_first_name('a' * 25), 'First name must be 24 characters or less.')
        # Test ime sa nevalidnim karakterima
        self.assertEqual(BaseUserValidator.validate_first_name('John123'), 'First name can only contain letters and spaces.')

    def test_validate_last_name(self):
        # Test validno prezime
        self.assertIsNone(BaseUserValidator.validate_last_name('Doe'))
        # Test prazno prezime
        self.assertEqual(BaseUserValidator.validate_last_name(''), 'Last name cannot be empty.')
        # Test predugo prezime
        self.assertEqual(BaseUserValidator.validate_last_name('a' * 25), 'Last name must be 24 characters or less.')
        # Test prezime sa nevalidnim karakterima
        self.assertEqual(BaseUserValidator.validate_last_name('Doe123'), 'Last name can only contain letters and spaces.')

    def test_validate_username(self):
        # Test validno korisničko ime
        self.assertIsNone(BaseUserValidator.validate_username('valid_username'))
        # Test prazno korisničko ime
        self.assertEqual(BaseUserValidator.validate_username(''), 'Username cannot be empty.')
        # Test predugo korisničko ime
        self.assertEqual(BaseUserValidator.validate_username('a' * 25), 'Username must be 24 characters or less.')
        # Test korisničko ime sa nevalidnim karakterima
        self.assertEqual(BaseUserValidator.validate_username('invalid-username'), 'Username can only contain letters, numbers, and underscores.')

    def test_validate_confirm_password(self):
        # Test kada lozinke odgovaraju
        self.assertIsNone(BaseUserValidator.validate_confirm_password('password123', 'password123'))
        # Test kada lozinke ne odgovaraju
        self.assertEqual(BaseUserValidator.validate_confirm_password('password123', 'differentpassword'), 'Passwords must match.')
        # Test nevalidne potvrde lozinke
        self.assertEqual(BaseUserValidator.validate_confirm_password('short', 'short'), 'Password must be between 8 and 64 characters long.')

    def test_validate_birth_date(self):
        # Test validan datum
        self.assertIsNone(BaseUserValidator.validate_birth_date(date(2000,1,1)))
        # Test prazno polje
        self.assertEqual(BaseUserValidator.validate_birth_date(''), 'Birth cannot be empty.')

if __name__ == '__main__':
    unittest.main()