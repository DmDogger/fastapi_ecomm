from fastapi_filter import FilterDepends
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import CategoryNotFound
from app.repositories.category_repo import CategoryRepository
from app.schemas import CategoryFilter
from fastapi_pagination.ext.sqlalchemy import paginate


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self._repository = repository

    async def find_all_active_categories(self):
        """ Находит все активные категории """
        categories = await self._repository.get_all()
        if not categories:
            return CategoryNotFound()
        return categories

    async def get_paginate_categories(self,
                                        filter_: CategoryFilter,
                                        params: Params
                                        ) :
        """ Находит и возвращает отфильтрованные / пагинированные категории """

        query = self._repository.get_query_for_pagination()


        query = filter_.filter(query)
        return await paginate(
            query=query,
            conn=self._repository.db,
            params=params
        )

    async def create_category(self, category):
        if category.parent_id is not None:
            parent = await self.find_parent_category(category.parent_id)
            if not parent:
                raise CategoryNotFound()
        category = await self._repository.create(category)
        return category


    async def find_parent_category(self, parent_id):
        parent = await self._repository.get_category_by_parent(parent_id)
        if not parent:
            raise CategoryNotFound()
        return parent