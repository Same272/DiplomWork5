from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, constr
import re
from telebot import TeleBot

bot = TeleBot(token='7722831734:AAHhjV00pbU5l0b_OL90il5G1UW_MV4h54Y')

from database.usersss import (
    register_user, authenticate_user, update_user_details, remove_user_account, add_to_wishlist,
    remove_from_cart, remove_from_wishlist, add_to_shopping_cart, list_all_products,
    filter_products_by_brand, filter_products_by_category, list_all_brands, list_all_categories,
    get_brand_details, get_product_details, get_category_details, create_offer,
)

user_router = APIRouter()

# Регулярные выражения для проверки email и номера телефона
email_check = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
phone_number_check = re.compile(r'^\+998(33|90|97|94)\d{7}$')

def mail_checker(email, phone_number):
    """Проверяет корректность email и номера телефона."""
    if re.fullmatch(email_check, email) and re.fullmatch(phone_number_check, phone_number):
        return True
    return False

# Модели запросов
class RegistrationModel(BaseModel):
    """Модель для регистрации нового пользователя."""
    username: str
    phone_number: str
    email: str
    password1: constr(max_length=10)
    password2: constr(max_length=10)
    address: Optional[str]

class LoginModel(BaseModel):
    """Модель для входа в аккаунт."""
    identificator: str
    password: str

class ChangeAccountModel(BaseModel):
    """Модель для изменения данных аккаунта."""
    id: int
    password: str
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    new_password: Optional[str] = None

class UserDeleteAccountModel(BaseModel):
    """Модель для удаления аккаунта."""
    id: int
    password: str
    reason: Optional[str] = None

class NewCategory(BaseModel):
    """Модель для создания новой категории."""
    name: str
    descr: str

class NewBrand(BaseModel):
    """Модель для создания нового бренда."""
    name: str
    descr: str

# Роуты
@user_router.post('/registration', tags=['Юзер сервис'])
async def user_registration(user_model: RegistrationModel):
    """
    Регистрация нового пользователя.
    """
    data = user_model.dict()
    checker = mail_checker(user_model.email, user_model.phone_number)
    if checker:
        result = register_user(**data)
        return {'status': 1, 'message': 'Пользователь успешно зарегистрирован!'}
    return {'status': 0, 'message': 'Некорректный email или номер телефона.'}

@user_router.post('/login', tags=['Юзер сервис'])
async def user_login(user_model: LoginModel):
    """
    Авторизация пользователя.
    """
    result = authenticate_user(identificator=user_model.identificator, password=user_model.password)
    return {'status': 1, 'message': 'Авторизация успешна', 'data': result}

@user_router.put('/account/update', tags=['Юзер сервис'])
async def user_update_account(user_model: ChangeAccountModel):
    """
    Изменение данных пользователя.
    """
    result = update_user_details(
        id=user_model.id,
        password=user_model.password,
        username=user_model.username,
        phone_number=user_model.phone_number,
        email=user_model.email,
        address=user_model.address,
        new_password=user_model.new_password
    )
    return {'status': 1, 'message': 'Данные аккаунта успешно обновлены', 'data': result}

@user_router.delete('/account/delete', tags=['Юзер сервис'])
async def user_delete_account(user_model: UserDeleteAccountModel):
    """
    Удаление аккаунта пользователя.
    """
    result = remove_user_account(id=user_model.id, password=user_model.password)
    return {'status': 1, 'message': 'Аккаунт успешно удален', 'data': result}

@user_router.get('/categories/{id}', tags=['Категории'])
async def get_category_details(id: int):
    """
    Получение данных конкретной категории.
    """
    result = get_category_details(id=id)
    return {'status': 1, 'message': 'Категория получена', 'data': result}

@user_router.get('/brands/{id}', tags=['Бренды'])
async def get_brand_details(id: int):
    """
    Получение данных конкретного бренда.
    """
    result = get_brand_details(id=id)
    return {'status': 1, 'message': 'Бренд получен', 'data': result}

@user_router.get('/products/{id}', tags=['Продукты'])
async def get_product_details(id: int):
    """
    Получение данных конкретного продукта.
    """
    result = get_product_details(id=id)
    return {'status': 1, 'message': 'Продукт получен', 'data': result}

@user_router.post('/favorites/add', tags=['Избранное'])
async def add_to_favorites(id: int, product_id: int):
    """
    Добавление товара в избранное.
    """
    result = add_to_wishlist(id=id, product_id=product_id)
    return {'status': 1, 'message': 'Товар добавлен в избранное', 'data': result}

@user_router.post('/cart/add', tags=['Корзина'])
async def add_to_shopping_cart(id: int, product_id: int, count: int):
    """
    Добавление товара в корзину.
    """
    result = add_to_shopping_cart(id=id, product_id=product_id, count=count)
    return {'status': 1, 'message': 'Товар добавлен в корзину', 'data': result}

@user_router.delete('/cart/delete', tags=['Корзина'])
async def delete_from_shopping_cart(id: int, product_id: int, count: int):
    """
    Удаление товара из корзины.
    """
    result = remove_from_cart(id=id, product_id=product_id, count=count)
    return {'status': 1, 'message': 'Товар удален из корзины', 'data': result}

@user_router.delete('/favorites/delete', tags=['Избранное'])
async def delete_from_favorites(id: int, product_id: int):
    """
    Удаление товара из избранного.
    """
    result = remove_from_wishlist(id=id, product_id=product_id)
    return {'status': 1, 'message': 'Товар удален из избранного', 'data': result}

@user_router.get('/home', tags=['Товары'])
async def get_home_page():
    """
    Получение списка всех товаров для главной страницы.
    """
    result = list_all_products()
    return {'status': 1, 'message': 'Главная страница товаров', 'data': result}

@user_router.get('/products/category/{id}', tags=['Категории'])
async def get_products_by_category(id: int):
    """
    Получение списка товаров по категории.
    """
    result = filter_products_by_category(id=id)
    return {'status': 1, 'message': 'Товары по категории получены', 'data': result}

@user_router.get('/products/brand/{id}', tags=['Бренды'])
async def get_products_by_brand(id: int):
    """
    Получение списка товаров по бренду.
    """
    result = filter_products_by_brand(id=id)
    return {'status': 1, 'message': 'Товары по бренду получены', 'data': result}

@user_router.get('/categories', tags=['Категории'])
async def get_all_categories():
    """
    Получение списка всех категорий.
    """
    result = list_all_categories()
    return {'status': 1, 'message': 'Все категории получены', 'data': result}

@user_router.get('/brands', tags=['Бренды'])
async def get_all_brands_list():
    """
    Получение списка всех брендов.
    """
    result = list_all_brands()
    return {'status': 1, 'message': 'Все бренды получены', 'data': result}

@user_router.post('/orders/new', tags=['Заказы'])
async def create_new_offer(id: int, count: int):
    """
    Создание нового заказа.
    """
    result = create_offer(id=id, count=count)
    if result:
        message = (
            f"\ud83d\udce6 *Новый заказ!*\n\n"
            f"\ud83c\udd94 *ID товара:* {id}\n"
            f"\ud83d\udce6 *Количество:* {count}\n"
            f"\ud83d\udcb0 *Цена:* {result.price * count} ₽\n\n"
            f"\ud83d\uded2 Спасибо за ваш заказ!"
        )
        with open(result.photo, "rb") as photo:
            bot.send_photo(
                chat_id=-4592099015,
                photo=photo,
                caption=message,
                parse_mode="Markdown"
            )
        return {'status': 1, 'message': 'Заказ успешно создан'}
    else:
        return {'status': 0, 'message': 'Ошибка при создании заказа'}