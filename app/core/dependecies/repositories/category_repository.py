from fastapi import Depends
from app.database import AsyncSession
from app.db_depends import get_async_db
from app.repositories.category_repo import CategoryRepository
from app.models.categories import Category as CategoryModel

def get_category_repository(
        session: AsyncSession = Depends(get_async_db)
) -> CategoryRepository:
    """ Конструкция CategoryRepository с внедренной AsyncSession """
    return CategoryRepository(db=session, model=CategoryModel)