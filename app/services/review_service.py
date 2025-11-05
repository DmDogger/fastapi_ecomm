from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User as UserModel
from app.models.reviews import Review as ReviewModel

from app.core.exceptions import ReviewNotFound, ProductNotFound, SellerCannotLeaveReview, CanReviewOnlyOnce
from app.repositories.products_repo import ProductRepository
from app.repositories.review_repo import ReviewRepository
from app.schemas import ReviewCreate as ReviewCreateSchema
from app.services.product_service import ProductService


class ReviewService:
    def __init__(self,
                 review_repository: ReviewRepository ,
                 product_repository: ProductRepository,
                 product_service: ProductService
                 ):
        self._review_repository = review_repository
        self._product_repository = product_repository
        self._product_service = product_service

    async def get_reviews(self):
        """ Returns review list """
        return await self._review_repository.get_all()


    async def create_review(self, review_data: ReviewCreateSchema,
                            user: UserModel):
        """ Method allows a user to leave a review for a product """
        if user.role == 'seller':
            raise SellerCannotLeaveReview()
        product = await self._product_repository.get(review_data.product_id)
        if not product:
            raise ProductNotFound()
        if await self.user_already_reviewed_product(product.id, user.id):
            raise CanReviewOnlyOnce()
        review_data = review_data.model_dump()
        review_data.update({'user_id': user.id})
        review = await self._review_repository.create(review_data)
        await self._product_service.push_product_rating(product.id)
        await self._review_repository.db.commit() # Обратить внимание! Нужно переделать, чтобы транзакциями управлял не сервис!
        await self._review_repository.db.refresh(review)
        return review



    async def find_active_review(review_id: int,
                                 db: AsyncSession):
        """ Метод находит активный отзыв и возвращает его """
        review = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id,
                                                      ReviewModel.is_active == True))
        if not review.first():
            raise ReviewNotFound()
        return review

    async def get_user_active_review(review_id: int,
                                     current_user: UserModel,
                                     db: AsyncSession) -> ReviewModel:
        """ Возвращает активный отзыв пользователя если он существует """
        review = await db.scalars(select(ReviewModel).where(ReviewModel.user_id == current_user.id,
                                                            ReviewModel.id == review_id,
                                             ReviewModel.is_active == True))
        review = review.first()
        if not review:
            raise ReviewNotFound()
        return review

    async def user_already_reviewed_product(self,
                                            product_id: int,
                                            user_id: int
                                            ) -> bool:
        """ Проверяет, оставлял ли пользователь отзыв или нет"""
        result = await self._review_repository.get_review_by_user(product_id, user_id)
        if result:
            return True
        return False

