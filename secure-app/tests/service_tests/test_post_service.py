import unittest
from unittest.mock import MagicMock, patch
from app.services.post_service import PostService
from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.services.exceptions import *
from app.repositories.exceptions import *
from app.dto.create_post_dto import CreatePostDTO
from app import create_app

class TestPostService(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.post_repository = MagicMock(PostRepository)
        self.service = PostService(self.post_repository)

    def tearDown(self):
        self.app_context.pop()

    @patch('app.services.post_service.DatabaseError')
    def test_get_all_posts_success(self, mock_database_error):
        mock_database_error.side_effect = DatabaseError
        self.post_repository.get_all.return_value = [Post(title="Post 1"), Post(title="Post 2")]

        result = self.service.get_all_posts()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Post 1")
        self.post_repository.get_all.assert_called_once()

    @patch('app.services.post_service.DatabaseError')
    def test_get_post_success(self, mock_database_error):
        mock_database_error.side_effect = DatabaseError
        post = Post(title="Post 1")
        self.post_repository.get_by_id.return_value = post

        result = self.service.get_post('1')

        self.assertEqual(result.title, "Post 1")
        self.post_repository.get_by_id.assert_called_once_with('1')

    @patch('app.services.post_service.DatabaseError')
    @patch('app.services.post_service.EntityNotFoundError')
    def test_get_post_not_found(self, mock_not_found_error, mock_database_error):
        mock_database_error.side_effect = DatabaseError
        mock_not_found_error.side_effect = EntityNotFoundError('Post','title','sdas')
        self.post_repository.get_by_id.side_effect = NotFoundError("Post",1)

        with self.assertRaises(EntityNotFoundError):
            self.service.get_post('1')

    @patch('app.services.post_service.CreatePostValidator')
    @patch('app.services.post_service.DatabaseError')
    def test_create_post_invalid_input(self, mock_database_error, mock_validator):
        mock_database_error.side_effect = DatabaseError
        mock_validator.validate.return_value = "Invalid input"

        post_dto = CreatePostDTO(title="", body="Content", user_id="1", categories=["Tech"])

        with self.assertRaises(InvalidInputException):
            self.service.create_post(post_dto)

        mock_validator.validate.assert_called_once_with(post_dto.__dict__)
        
    @patch('app.services.post_service.CreatePostValidator')
    @patch('app.services.post_service.Post')
    @patch('app.services.post_service.DatabaseError')
    def test_create_post_success(self, mock_database_error, mock_post_class, mock_validator):
        mock_database_error.side_effect = DatabaseError
        mock_validator.validate.return_value = None

        mock_post_instance = MagicMock(spec=Post)
        mock_post_instance.title = "New Post"
        mock_post_instance.body = "Content"
        mock_post_instance.user_id = "1"
        mock_post_instance.categories = ["Tech"]

        mock_post_class.return_value = mock_post_instance

        post_dto = CreatePostDTO(title="New Post", body="Content", user_id="1", categories=["Tech"])
        self.post_repository.create.return_value = mock_post_instance

        result = self.service.create_post(post_dto)

        self.assertEqual(result.title, "New Post")
        self.assertEqual(result.body, "Content")
        self.assertEqual(result.user_id, "1")
        self.assertEqual(result.categories, ["Tech"])

        mock_validator.validate.assert_called_once_with(post_dto.__dict__)
        
        self.post_repository.create.assert_called_once_with(mock_post_instance)
    @patch('app.services.post_service.DatabaseError')
    def test_post_count_success(self, mock_database_error):
        mock_database_error.side_effect = DatabaseError
        self.post_repository.count.return_value = 5

        result = self.service.post_count()
        
        self.assertEqual(result, 5)
        self.post_repository.count.assert_called_once()
