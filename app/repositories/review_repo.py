from app.repositories.base_repo import BaseSQLRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update
from app.database import Base
from app.models.reviews import Review as ReviewModel

# Repository for reviews works with ORM-models

class ReviewRepository(BaseSQLRepository):
    def __init__(self, db: AsyncSession, model: Base):
        super().__init__(db, model)

    async def create(self, **kwargs):
        review = ReviewModel(**kwargs)
        self.db.add(review)
        return review

    async def get(self, id_: int):
        stmt = select(ReviewModel).where(ReviewModel.id == id_,
                                         ReviewModel.is_active == True)
        return await self.db.scalar(stmt)

    async def get_all(self):
        stmt = select(ReviewModel).where(ReviewModel.is_active == True)
        result = await self.db.scalars(stmt)
        result = result.all()
        if not result:
            return None
        return result

    async def get_reviews_by_product_id(self, id_: int):
        stmt = select(ReviewModel).where(ReviewModel.product_id == id_,
                                         ReviewModel.is_active == True)
        result = await self.db.scalars(stmt)
        result = result.all()
        return result


    async def update(self, id_: int, updated_data: dict):
        stmt = (
            sql_update(ReviewModel)
            .where(ReviewModel.id == id_,
                       ReviewModel.is_active == True)
            .values(**updated_data)
        )
        await self.db.execute(stmt)
        return self.get(id_)

    async def delete(self, id_):
        stmt = select(ReviewModel).where(ReviewModel.id == id_,
                                         ReviewModel.is_active == True)
        review = self.db.scalar(stmt)
        if not review:
            return None
        review.is_active = False
        self.db.add(review)
        return review


