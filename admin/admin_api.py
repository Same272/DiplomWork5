from fastapi import APIRouter, Form, File, UploadFile
from database.adminsss import (
    create_category, create_product, create_brand, get_user_by_id,
    delete_product, update_product, update_brand, delete_brand,
    delete_category, update_category
)
from pydantic import BaseModel
from typing import Optional
import uuid
import shutil

admin_router = APIRouter()

class NewBrand(BaseModel):
    name: str
    descr: str

class NewCategory(BaseModel):
    name: str
    descr: str

@admin_router.get('/users/{id}', tags=['Админ сервис'])
async def get_user_by_id_route(id: int):
    """
    Получение данных пользователя по ID.
    """
    result = get_user_by_id(id=id)
    if result:
        return {'status': 1, 'message': result}
    return {'status': 0, 'message': 'Пользователь не найден'}

@admin_router.post('/brands', tags=['Бренды'])
async def create_brand_route(brand_model: NewBrand):
    """
    Создание нового бренда.
    """
    result = create_brand(name=brand_model.name, descr=brand_model.descr)
    return {'status': 1, 'message': 'Бренд успешно создан', 'data': result}

@admin_router.post('/categories', tags=['Категории'])
async def create_category_route(category_model: NewCategory):
    """
    Создание новой категории.
    """
    result = create_category(name=category_model.name, descr=category_model.descr)
    return {'status': 1, 'message': 'Категория успешно создана', 'data': result}

@admin_router.post('/products', tags=['Товары'])
async def create_product_route(
    name: str = Form(...),
    descr: str = Form(...),
    price: str = Form(...),
    count: int = Form(...),
    category_id: int = Form(...),
    brand_id: int = Form(...),
    file: UploadFile = File(...)
):
    """
    Создание нового товара.
    """
    try:
        file_id = uuid.uuid4()
        file_extension = file.filename.split('.')[-1]
        file_path = f'database/photos/photo_{file_id}.{file_extension}'
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = create_product(
            name=name, descr=descr, photo=file_path, price=price,
            category_id=category_id, brand_id=brand_id, count=count
        )
        return {'status': 1, 'message': 'Товар успешно создан', 'data': result}
    except Exception as e:
        return {'status': 0, 'message': f'Ошибка: {str(e)}'}

@admin_router.put('/products/{id}', tags=['Товары'])
async def update_product_route(
    id: int,
    name: Optional[str] = Form(None),
    descr: Optional[str] = Form(None),
    price: Optional[str] = Form(None),
    count: Optional[int] = Form(None),
    category_id: Optional[int] = Form(None),
    brand_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Обновление данных товара.
    """
    try:
        file_path = None
        if file:
            file_id = uuid.uuid4()
            file_extension = file.filename.split('.')[-1]
            file_path = f'database/photos/photo_{file_id}.{file_extension}'
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)

        result = update_product(
            id=id, name=name, descr=descr, photo=file_path,
            price=price, count=count, category_id=category_id, brand_id=brand_id
        )
        return {'status': 1, 'message': 'Товар успешно обновлен', 'data': result}
    except Exception as e:
        return {'status': 0, 'message': f'Ошибка: {str(e)}'}

@admin_router.delete('/products/{id}', tags=['Товары'])
async def delete_product_route(id: int):
    """
    Удаление товара по ID.
    """
    result = delete_product(id=id)
    return {'status': 1, 'message': 'Товар успешно удален', 'data': result}

@admin_router.put('/brands/{id}', tags=['Бренды'])
async def update_brand_route(id: int, name: Optional[str] = None, descr: Optional[str] = None):
    """
    Обновление данных бренда.
    """
    result = update_brand(id=id, name=name, descr=descr)
    return {'status': 1, 'message': 'Бренд успешно обновлен', 'data': result}

@admin_router.put('/categories/{id}', tags=['Категории'])
async def update_category_route(id: int, name: Optional[str] = None, descr: Optional[str] = None):
    """
    Обновление данных категории.
    """
    result = update_category(id=id, name=name, descr=descr)
    return {'status': 1, 'message': 'Категория успешно обновлена', 'data': result}

@admin_router.delete('/categories/{id}', tags=['Категории'])
async def delete_category_route(id: int):
    """
    Удаление категории по ID.
    """
    result = delete_category(id=id)
    return {'status': 1, 'message': 'Категория успешно удалена', 'data': result}

@admin_router.delete('/brands/{id}', tags=['Бренды'])
async def delete_brand_route(id: int):
    """
    Удаление бренда по ID.
    """
    result = delete_brand(id=id)
    return {'status': 1, 'message': 'Бренд успешно удален', 'data': result}
