from fastapi import APIRouter, Depends
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependecies.services.review_service import get_review_service
from app.core.exceptions import ProductNotFound, SellerCannotLeaveReview, CanReviewOnlyOnce, ReviewNotFound

from app.auth import get_current_user, get_current_admin

from app.schemas import ReviewCreate as ReviewCreateSchema, Review as ReviewSchema
from app.models.reviews import Review as ReviewModel
from app.models.users import User as UserModel
from app.repositories.review_repo import ReviewRepository
from app.db_depends import get_async_db
from app.services.review_service import ReviewService

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

@router.get('/', status_code=200)
async def get_all_reviews(review_service: ReviewService = Depends(get_review_service)):
    """ Return list of reviews """
    return await review_service.get_reviews()

@router.post('/', response_model=ReviewSchema, status_code=201)
async def create_review(review_data: ReviewCreateSchema,
                        review_service: ReviewService = Depends(get_review_service),
                        user: UserModel = Depends(get_current_user)):
    return await review_service.create_review(review_data, user)

@router.delete('/{review_id}', status_code=200)
async def delete_review(review_id: int,
                        current_user_admin: UserModel = Depends(get_current_admin),
                        db: AsyncSession = Depends(get_async_db)):
    """ Метод позволяет удалить отзыв """
    review = await find_active_review(review_id, db)
    if not review:
        raise ReviewNotFound()
    product = await find_active_product(review.product_id, db)
    if not product:
        raise ProductNotFound()

    review.is_active=False

    await db.commit()
    await db.refresh(review)
    await push_product_rating(product.id, db)
    return {"message": f"review with ID: {review_id} was deleted successfully"}










