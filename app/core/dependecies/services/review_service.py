from fastapi import Depends

from app.core.dependecies.repositories.product_repository import get_product_repository
from app.core.dependecies.repositories.review_repository import get_review_repository
from app.core.dependecies.services import product_service
from app.core.dependecies.services.product_service import get_product_service
from app.repositories.products_repo import ProductRepository
from app.repositories.review_repo import ReviewRepository
from app.services.product_service import ProductService

from app.services.review_service import ReviewService


def get_review_service(
        review_repository:ReviewRepository = Depends(get_review_repository),
        product_repository: ProductRepository = Depends(get_product_repository),
        product_service: ProductService = Depends(get_product_service)
) -> ReviewService:
    """
    Создает экземпляр ReviewService с внедренными репозиториями.
    """
    return ReviewService(review_repository, product_repository, product_service)