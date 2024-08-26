from typing import Optional, List

from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.dto.create_post_dto import CreatePostDTO

from app.services.exceptions import *
from app.repositories.exceptions import *

from app.services.validators.create_post_validator import CreatePostValidator

class PostService:
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository


    def get_all_posts(self) -> List[Post]:
        """
        Retrieves all posts.

        Returns:
            List[Post]: A list of all post objects.

        Raises:
            DatabaseServiceError: If there is a database error.
        """
        try:
            return self.post_repository.get_all()
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def get_post(self, post_id: str) -> Optional[Post]:
        """
        Retrieves a post by their ID.

        Args:
            post_id (str): The ID of the post to retrieve.

        Returns:
            Optional[Post]: The post object if found, otherwise None.

        Raises:
            InvalidParameterException: If the post_id is invalid or missing.
            EntityNotFoundError: If the post is not found.
            DatabaseServiceError: If there is a database error.
        """
        try:
            post = self.post_repository.get_by_id(post_id)
            return post
        except NotFoundError as e:
            raise EntityNotFoundError("Post", "ID", post_id)
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e


    def create_post(self, post_dto: CreatePostDTO) -> Post:
        """
        Creates a new post.

        Args:
            post_dto (CreatePostDTO): The data transfer object containing post information.

        Returns:
            Post: The created post object.

        Raises:
            InvalidInputException: If the post_dto is invalid or missing.
            DatabaseServiceError: If there is a database error.
        """      
        msg = CreatePostValidator.validate(post_dto.__dict__)

        if msg:
            raise InvalidInputException('create post', 'Invalid or missing input')

        try:
            new_post = Post(
                title=post_dto.title, 
                body=post_dto.body, 
                user_id=post_dto.user_id, 
                categories=post_dto.categories
            )

            return self.post_repository.create(new_post)
        
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e

    def post_count(self) -> int:
        """
        Retrieves the total count of posts.

        Returns:
            int: The total number of posts.

        Raises:
            DatabaseServiceError: If there is a database error.
        """
        try:
            return self.post_repository.count()
        except DatabaseError as e:
            raise DatabaseServiceError(e) from e