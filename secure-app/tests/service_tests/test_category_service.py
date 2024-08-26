import unittest
from unittest.mock import MagicMock
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.models.post import Category
from app.services.exceptions import *
from app.repositories.exceptions import DatabaseError

class TestCategoryService(unittest.TestCase):
    def setUp(self):
        self.category_repository = MagicMock(CategoryRepository)
        self.service = CategoryService(self.category_repository)

    def test_get_all_categories(self):
        categories = [Category(id='1', name='Technology'), Category(id='2', name='Science')]
        self.category_repository.get_all.return_value = categories

        result = self.service.get_all_categories()
        self.assertEqual(result, categories)
        self.category_repository.get_all.assert_called_once()

    def test_get_all_categories_database_error(self):
        self.category_repository.get_all.side_effect = DatabaseError('Database error')
        
        with self.assertRaises(DatabaseServiceError):
            self.service.get_all_categories()

    def test_get_category_by_id_valid(self):
        category = Category(id='1', name='Technology')
        self.category_repository.get_by_id.return_value = category

        result = self.service.get_category_by_id('1')
        self.assertEqual(result, category)
        self.category_repository.get_by_id.assert_called_once_with('1')

    def test_get_category_by_id_invalid_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.get_category_by_id(None)

    def test_get_category_by_id_not_found(self):
        self.category_repository.get_by_id.return_value = None
        
        with self.assertRaises(EntityNotFoundError):
            self.service.get_category_by_id('1')

    def test_get_category_by_id_database_error(self):
        self.category_repository.get_by_id.side_effect = DatabaseError('Database error')
        
        with self.assertRaises(DatabaseServiceError):
            self.service.get_category_by_id('1')