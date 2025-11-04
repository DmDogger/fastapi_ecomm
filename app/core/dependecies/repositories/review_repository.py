from fastapi import Depends
from app.database import AsyncSession
from app.db_depends import get_async_db
from app.models.reviews import Review as ReviewModel
from app.repositories.review_repo import ReviewRepository
from app.services.product_service import ProductService


def get_review_repository(
        session: AsyncSession = Depends(get_async_db)
) -> ReviewRepository:
    """ Конструкция ProductRepository с внедренной AsyncSession """
    return ReviewRepository(db=session, model=ReviewModel)