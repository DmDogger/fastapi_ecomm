from fastapi_pagination import Params
from app.core.exceptions import CategoryNotFound
from app.repositories.category_repo import CategoryRepository
from app.schemas import CategoryFilter, CategoryCreate as CategoryCreateSchema
from fastapi_pagination.ext.sqlalchemy import paginate



class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self._repository = repository

    async def find_parent_category(self, parent_id):
        """ Finds a parent category """
        parent = await self._repository.get_category_by_parent(parent_id)
        if not parent:
            raise CategoryNotFound()
        return parent

    async def find_all_active_categories(self):
        """ Finds all active categories """
        categories = await self._repository.get_all()
        if not categories:
            return CategoryNotFound()
        return categories

    async def get_paginate_categories(self,
                                        filter_: CategoryFilter,
                                        params: Params
                                        ) :
        """ Finds and return filtered & paginated categories """

        query = self._repository.get_query_for_pagination()


        query = filter_.filter(query)
        return await paginate(
            query=query,
            conn=self._repository.db,
            params=params
        )

    async def create_category(self, category: CategoryCreateSchema):
        """ Business logic for creating category in database """
        if category.parent_id is not None:
            parent = await self.find_parent_category(category.parent_id)
            if not parent:
                raise CategoryNotFound()
        category = await self._repository.create(category)
        return category

    async def update_category(self, category: CategoryCreateSchema, id_: int):
        """ Business logic for updating category in database"""
        db_category = await self._repository.get(id_)
        if not db_category:
            raise CategoryNotFound()

        if category.parent_id is not None:
            parent = await self.find_parent_category(category.parent_id)
            if not parent:
                raise CategoryNotFound()

        update_data = category.model_dump()
        updated_db_data = await self._repository.update(id_, update_data)
        return updated_db_data

    async def delete_category(self, id_: int):
        category = await self._repository.get(id_)
        if not category:
            raise CategoryNotFound()
        await self._repository.delete(id_)

