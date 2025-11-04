from fastapi import Depends

from app.core.dependecies.repositories.product_repository import get_product_repository
from app.core.dependecies.repositories.category_repository import get_category_repository
from app.core.dependecies.repositories.review_repository import get_review_repository

from app.repositories.products_repo import ProductRepository
from app.repositories.category_repo import CategoryRepository
from app.repositories.review_repo import ReviewRepository
from app.services.product_service import ProductService


def get_product_service(
        product_repository: ProductRepository = Depends(get_product_repository),
        review_repository: ReviewRepository = Depends(get_review_repository),
        category_repository: CategoryRepository = Depends(get_category_repository)

) -> ProductService:
    """
    Создает экземпляр ProductService с внедренными репозиториями.
    """
    return ProductService(
        product_repository=product_repository,
        review_repository=review_repository,
        category_repository=category_repository
    )