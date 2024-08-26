import unittest
from unittest.mock import MagicMock, patch
from app.services.author_requests_service import AuthorRequestsService
from app.repositories import AuthorRequestsRepository, UserRepository
from app.services.exceptions import *
from app.repositories.exceptions import *
from app.models import AuthorRequests

class TestAuthorRequestsService(unittest.TestCase):
    def setUp(self):
        self.author_requests_repository = MagicMock(AuthorRequestsRepository)
        self.user_repository = MagicMock(UserRepository)
        self.service = AuthorRequestsService(self.author_requests_repository, self.user_repository)

    def test_create_author_request_valid(self):
        user_id = '123'
        author_request = AuthorRequests(user_id=user_id)
        ret_val = AuthorRequests(user_id=user_id, status='InProgress')
        self.author_requests_repository.create.return_value = ret_val

        result = self.service.create_author_request(user_id)
        self.assertEqual(result, ret_val)
       

    def test_create_author_request_missing_user_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.create_author_request(None)
    
    def test_create_author_request_database_error(self):
        self.author_requests_repository.create.side_effect = DatabaseError('Database error')
        
        with self.assertRaises(DatabaseServiceError):
            self.service.create_author_request('123')

    def test_check_existence_valid(self):
        user_id = '123'
        self.author_requests_repository.check_request.return_value = True

        result = self.service.check_existence(user_id)
        self.assertTrue(result)
        self.author_requests_repository.check_request.assert_called_once_with(user_id)

    def test_check_existence_missing_user_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.check_existence(None)
    
    def test_check_existence_database_error(self):
        self.author_requests_repository.check_request.side_effect = DatabaseError('Database error')
        
        with self.assertRaises(DatabaseServiceError):
            self.service.check_existence('123')

    def test_get_all_author_requests(self):
        author_requests = [AuthorRequests(user_id='123')]
        self.author_requests_repository.get_all.return_value = author_requests

        result = self.service.get_all_author_requests()
        self.assertEqual(result, author_requests)
        self.author_requests_repository.get_all.assert_called_once()

    def test_get_all_author_requests_database_error(self):
        self.author_requests_repository.get_all.side_effect = DatabaseError('Database error')
        
        with self.assertRaises(DatabaseServiceError):
            self.service.get_all_author_requests()

    def test_update_request_valid(self):
        request_id = '123'
        status = 'approved'
        author_request = AuthorRequests(user_id='123')
        self.author_requests_repository.update_request.return_value = author_request

        result = self.service.update_request(request_id, status)
        self.assertEqual(result, author_request)
        self.author_requests_repository.update_request.assert_called_once_with(request_id, status)

    def test_update_request_missing_request_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_request(None, 'approved')
    
    def test_update_request_missing_status(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_request('123', None)
    
    def test_update_request_not_found(self):
        self.author_requests_repository.update_request.side_effect = NotFoundError('some_user', '1234')
        
        with self.assertRaises(EntityNotFoundError):
            self.service.update_request('123', 'approved')
    
    def test_update_request_database_error(self):
        self.author_requests_repository.update_request.side_effect = DatabaseError('Database error')
        
        with self.assertRaises(DatabaseServiceError):
            self.service.update_request('123', 'approved')