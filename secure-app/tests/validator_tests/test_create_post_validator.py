import unittest
from app.services.validators.create_post_validator import CreatePostValidator
class TestCreatePostValidator(unittest.TestCase):
    def test_validate_success(self):
        data = {
            'title': 'Valid Title',
            'body': 'This is a valid body content.',
            'categories': ['Category1', 'Category2']
        }
        result = CreatePostValidator.validate(data)
        self.assertIsNone(result)

    def test_validate_missing_title(self):
        data = {
            'body': 'This is a valid body content.',
            'categories': ['Category1', 'Category2']
        }
        result = CreatePostValidator.validate(data)
        self.assertEqual(result, 'Title cannot be empty.')

    def test_validate_long_title(self):
        data = {
            'title': 'A' * 129,  # Title length > 128
            'body': 'This is a valid body content.',
            'categories': ['Category1', 'Category2']
        }
        result = CreatePostValidator.validate(data)
        self.assertEqual(result, 'Title must be 128 characters or less.')

    def test_validate_missing_body(self):
        data = {
            'title': 'Valid Title',
            'categories': ['Category1', 'Category2']
        }
        result = CreatePostValidator.validate(data)
        self.assertEqual(result, 'Body cannot be empty.')

    def test_validate_empty_categories(self):
        data = {
            'title': 'Valid Title',
            'body': 'This is a valid body content.',
            'categories': []  # Empty list
        }
        result = CreatePostValidator.validate(data)
        self.assertEqual(result, 'Category cannot be empty.')

    def test_validate_invalid_categories(self):
        data = {
            'title': 'Valid Title',
            'body': 'This is a valid body content.',
            'categories': 'Invalid Category List'  # Not a list
        }
        result = CreatePostValidator.validate(data)
        self.assertEqual(result, 'Categories must be a list.')

if __name__ == '__main__':
    unittest.main()