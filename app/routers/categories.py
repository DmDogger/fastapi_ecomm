from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params

from app.schemas import Category as CategoryResponseSchema, CategoryCreate as CategoryCreateSchema, CategoryOut, CategoryFilter
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
                          category_service: CategoryService = Depends(get_category_service)):
    """
    Обновляет выбранную категорию по ее ID
    """
    updated_category = await category_service.update_category(category, category_id)
    return updated_category



@router.delete('/{category_id}', status_code=200)
async def delete_category(category_id: int,
                          category_service: CategoryService = Depends(get_category_service)):
    """
    Удаляет категорию по ее ID
    """
    await category_service.delete_category(category_id)
    return {'message': f'category with ID: {category_id} was deleted successfully'}


