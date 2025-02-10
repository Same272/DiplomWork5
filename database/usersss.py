from database import get_db, Base
from database.models import Account, ProductCategory, ProductBrand, Item, ShoppingCart, Wishlist
from telebot import TeleBot
bot = TeleBot(token='YOUR_BOT_TOKEN')

# Функция регистрации нового пользователя
def register_user(username: str, pass1: str, pass2: str, phone: str, mail: str = None, addr: str = None):
    """
    Регистрирует нового пользователя.
    Проверяет существование пользователя по номеру телефона или email.
    Создает учетную запись, если пароли совпадают.
    """
    with next(get_db()) as db:
        existing_user = db.query(Account).filter(
            (Account.phone_number == phone) |
            (Account.email == mail)
        ).first()
        if existing_user:
            return {"status": 0, 'message': "User already registered"}
        else:
            if pass1 == pass2:
                new_user = Account(
                    username=username,
                    password=pass1,
                    phone_number=phone,
                    email=mail,
                    address=addr,
                )
                db.add(new_user)
                db.commit()
                return {"status": 1, 'message': 'Registration successful'}
            return {"status": 0, 'message': 'Passwords do not match'}

# Функция аутентификации пользователя
def authenticate_user(identifier: str, passwd: str):
    """
    Проверяет учетные данные пользователя (телефон или email и пароль).
    Возвращает сообщение об успешной авторизации или ошибке.
    """
    with next(get_db()) as db:
        user = db.query(Account).filter(
            (Account.phone_number == identifier) |
            (Account.email == identifier)
        ).first()
        if not user:
            return {'status': 0, 'message': 'User not found'}
        if user.password == passwd:
            return {'status': 1, 'message': 'Login successful'}
        return {'status': 0, 'message': 'Incorrect password'}

# Функция обновления данных пользователя
def update_user_details(user_id: int, passwd: str, uname: str = None, phone: str = None, mail: str = None,
                        addr: str = None, new_pass: str = None):
    """
    Обновляет данные пользователя (имя, телефон, email, адрес или пароль).
    Проверяет корректность текущего пароля перед внесением изменений.
    """
    with next(get_db()) as db:
        user = db.query(Account).filter_by(id=user_id).first()
        modified = False
        if not user:
            return {'status': 0, 'message': 'User not found'}
        if user.password == passwd:
            if uname and uname != 'string':
                user.username = uname
                modified = True
            if phone and phone != 'string':
                user.phone_number = phone
                modified = True
            if mail and mail != 'string':
                user.email = mail
                modified = True
            if addr and addr != 'string':
                user.address = addr
                modified = True
            if new_pass and new_pass != 'string':
                user.password = new_pass
                modified = True

            if modified:
                db.commit()
                return {'status': 1, 'message': 'User details updated'}
            else:
                return {'status': 0, 'message': 'No changes detected'}
        else:
            return {'status': 0, 'message': "Invalid password"}

# Функция удаления аккаунта пользователя
def remove_user_account(user_id: int, passwd: str):
    """
    Удаляет аккаунт пользователя, если указан правильный пароль.
    """
    with next(get_db()) as db:
        user = db.query(Account).filter_by(id=user_id).first()
        if user and user.password == passwd:
            db.delete(user)
            db.commit()
            return {'status': 1, 'message': 'Account deleted'}
        return {"status": 0, 'message': 'Error deleting account'}

# Функция добавления товара в избранное
def add_to_wishlist(user_id: int, product_id: int):
    """
    Добавляет товар в список избранного для указанного пользователя.
    """
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=product_id).first()
        if product:
            new_fav = Wishlist(
                user_id=user_id,
                product_id=product_id
            )
            db.add(new_fav)
            db.commit()
            return {'status': 1, 'message': 'Added to wishlist'}
        return {'status': 0, 'message': 'Product not found'}

# Функция удаления товара из избранного
def remove_from_wishlist(user_id: int, product_id: int):
    """
    Удаляет товар из списка избранного пользователя.
    """
    with next(get_db()) as db:
        fav = db.query(Wishlist).filter_by(user_id=user_id, product_id=product_id).one_or_none()
        if fav:
            db.delete(fav)
            db.commit()
            return {'status': 1, 'message': 'Removed from wishlist'}
        return {'status': 0, 'message': 'Item not in wishlist'}

# Функция добавления товара в корзину
def add_to_shopping_cart(user_id: int, product_id: int, qty: int):
    """
    Добавляет товар в корзину пользователя. Если товар уже есть, обновляет количество.
    """
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=product_id).first()
        cart_item = db.query(ShoppingCart).filter_by(product_id=product_id, user_id=user_id).first()
        if product and cart_item:
            cart_item.count += qty
            db.commit()
            return {'status': 1, 'message': 'Cart updated'}
        elif product and not cart_item:
            new_cart_item = ShoppingCart(
                user_id=user_id,
                product_id=product_id,
                count=qty
            )
            db.add(new_cart_item)
            db.commit()
            return {'status': 1, 'message': 'Item added to cart'}
        else:
            return {'status': 0, 'message': 'Product not found'}

# Функция удаления товара из корзины
def remove_from_cart(user_id: int, product_id: int, qty: int):
    """
    Уменьшает количество товара в корзине или полностью удаляет товар, если количество становится равным нулю.
    """
    with next(get_db()) as db:
        cart_item = db.query(ShoppingCart).filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            if cart_item.count > qty:
                cart_item.count -= qty
                db.commit()
            else:
                db.delete(cart_item)
                db.commit()
            return {'status': 1, 'message': 'Cart updated'}
        return {'status': 0, 'message': 'Item not in cart'}

# Функция получения списка всех товаров
def list_all_products():
    """
    Возвращает список всех доступных товаров.
    """
    with next(get_db()) as db:
        return db.query(Item).all()

# Функция фильтрации товаров по бренду
def filter_products_by_brand(brand_id: int):
    """
    Возвращает список товаров, относящихся к указанному бренду.
    """
    with next(get_db()) as db:
        return db.query(Item).filter_by(brand_id=brand_id).all()

# Функция фильтрации товаров по категории
def filter_products_by_category(cat_id: int):
    """
    Возвращает список товаров, относящихся к указанной категории.
    """
    with next(get_db()) as db:
        return db.query(Item).filter_by(category_id=cat_id).all()

# Функция получения списка всех категорий
def list_all_categories():
    """
    Возвращает список всех категорий товаров.
    """
    with next(get_db()) as db:
        return db.query(ProductCategory).all()

# Функция получения списка всех брендов
def list_all_brands():
    """
    Возвращает список всех брендов товаров.
    """
    with next(get_db()) as db:
        return db.query(ProductBrand).all()

# Функция получения подробностей о товаре
def get_product_details(prod_id: int):
    """
    Возвращает информацию о конкретном товаре.
    """
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=prod_id).first()
        if product:
            return product
        return {'status': 0, 'message': 'Product not found'}

# Функция получения подробностей о бренде
def get_brand_details(brand_id: int):
    """
    Возвращает информацию о конкретном бренде.
    """
    with next(get_db()) as db:
        brand = db.query(ProductBrand).filter_by(id=brand_id).first()
        if brand:
            return brand
        return {'status': 0, 'message': 'Brand not found'}

# Функция получения подробностей о категории
def get_category_details(cat_id: int):
    """
    Возвращает информацию о конкретной категории товаров.
    """
    with next(get_db()) as db:
        category = db.query(ProductCategory).filter_by(id=cat_id).first()
        if category:
            return category
        return {'status': 0, 'message': 'Category not found'}

# Функция получения деталей корзины
def get_cart_details(cart_id: int):
    """
    Возвращает информацию о конкретной корзине.
    """
    with next(get_db()) as db:
        cart = db.query(ShoppingCart).filter_by(id=cart_id).first()
        if cart:
            return cart
        return {'status': 0, 'message': 'Cart not found'}

# Функция создания предложения
def create_offer(prod_id: int, qty: int):
    """
    Возвращает товар для создания предложения с указанным количеством.
    """
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=prod_id).first()
        return product
