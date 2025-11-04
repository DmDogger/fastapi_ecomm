from fastapi import Depends

from app.core.dependecies.repositories.category_repository import get_category_repository
from app.repositories.category_repo import CategoryRepository
from app.services.category_service import CategoryService


def get_category_service(
        repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    """
    Constructs an CategoryService instance with injected CategoryRepository.
    """
    return CategoryService(repository)