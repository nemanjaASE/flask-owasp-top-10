import unittest
from unittest.mock import patch, MagicMock
from app.services.otp_token_service import OTPTokenService
from app.services.exceptions import InvalidInputException
from itsdangerous import SignatureExpired, BadSignature

class TestOTPTokenService(unittest.TestCase):
    def setUp(self):
        self.s = 'secret'
        self.service = OTPTokenService(self.s)

    @patch('app.utils.token_utils.verify_otp_token')
    def test_verify_otp_token_success(self, mock_verify_otp_token):
        mock_verify_otp_token.return_value = 'valid_otp'

        otp_token = 'valid_token'
        result = self.service.verify_otp_token(otp_token)
        
        self.assertEqual(result, 'valid_otp')
        mock_verify_otp_token.assert_called_once_with(otp_token, self.s)

    def test_verify_otp_token_missing_token(self):
        with self.assertRaises(InvalidInputException):
            self.service.verify_otp_token(None)

    @patch('app.utils.token_utils.verify_otp_token')
    def test_verify_otp_token_signature_expired(self, mock_verify_otp_token):
        mock_verify_otp_token.side_effect = SignatureExpired('Token expired')

        with self.assertRaises(SignatureExpired):
            self.service.verify_otp_token('expired_token')

    @patch('app.utils.token_utils.verify_otp_token')
    def test_verify_otp_token_bad_signature(self, mock_verify_otp_token):
        mock_verify_otp_token.side_effect = BadSignature('Invalid signature')

        with self.assertRaises(BadSignature):
            self.service.verify_otp_token('bad_signature_token')

    @patch('app.utils.token_utils.verify_otp_token')
    def test_verify_otp_token_other_exception(self, mock_verify_otp_token):
        mock_verify_otp_token.side_effect = Exception('Other error')

        with self.assertRaises(Exception):
            self.service.verify_otp_token('other_exception_token')
