from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategoryResponseSchema, CategoryCreate as CategoryCreateSchema, CategoryOut, CategoryFilter
from app.db_depends import get_async_db

from app.core.exceptions import CategoryNotFound
from app.core.dependecies.services.category_service import CategoryService, get_category_service

router = APIRouter(
    prefix='/categories',
    tags=['categories']
                   )

@router.get('/', response_model=Page[CategoryOut], status_code=200)
async def get_category(category_service: CategoryService = Depends(get_category_service),
                       filter_: CategoryFilter = FilterDepends(CategoryFilter),
                       params: Params = Depends()):
    """
    Возвращает список категорий.
    """
    categories = await category_service.get_paginate_categories(filter_=filter_, params=params)
    return categories

@router.post('/', response_model=CategoryResponseSchema, status_code=201)
async def create_category(category: CategoryCreateSchema,
                          category_service: CategoryService = Depends(get_category_service)):
    """
    Создает новую категорию
    """
    category = await category_service.create_category(category)
    return category


@router.put('/{category_id}', response_model=CategoryResponseSchema, status_code=200)
async def update_category(category_id: int,
                          category: CategoryCreateSchema,
                          db: AsyncSession = Depends(get_async_db)):
    """
    Обновляет выбранную категорию по ее ID
    """
    # Проверка существования категории
    db_category = await find_category(category_id, db)
    if db_category is None:
        raise CategoryNotFound()

    # Проверка существования parent_id если указан
    if category.parent_id is not None:
        cursor = await db.scalars(select(CategoryModel).where(CategoryModel.id == category.parent_id,
                                                              CategoryModel.is_active == True))
        parent_id = cursor.first()
        if parent_id is None:
            raise CategoryNotFound()

    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)

    await db.commit()
    await db.refresh(db_category)
    return db_category




@router.delete('/{category_id}', status_code=200)
async def delete_category(category_id: int,
                          db: AsyncSession = Depends(get_async_db)):
    """
    Удаляет категорию по ее ID
    """
    # --- проверка существования категории ---
    category = await find_category(category_id, db)
    if category is None:
        raise CategoryNotFound()
    # --- обновляем статус категории на is_active = False ---
    category.is_active = False
    await db.commit()
    return {"status":"success", "message": f"category {category_id} is unactive"}



