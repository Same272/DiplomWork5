from database import get_db, Base
from database.models import Account, ProductCategory, ProductBrand, Item, ShoppingCart, Wishlist

# Создание новой категории
def create_category(name: str, description: str):
    """
    Создает новую категорию в базе данных.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        existing_category = db.query(ProductCategory).filter_by(name=name).first()
        if existing_category:
            return {'status': 0, 'message': 'Категория уже существует'}
        new_category = ProductCategory(name=name, descr=description)
        db.add(new_category)
        db.commit()
        return {'status': 1, 'message': 'Категория успешно создана'}

# Создание нового бренда
def create_brand(name: str, description: str):
    """
    Создает новый бренд в базе данных.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        existing_brand = db.query(ProductBrand).filter_by(name=name).first()
        if existing_brand:
            return {'status': 0, 'message': 'Бренд уже существует'}
        new_brand = ProductBrand(name=name, descr=description)
        db.add(new_brand)
        db.commit()
        return {'status': 1, 'message': 'Бренд успешно создан'}

# Создание нового продукта
def create_product(name: str, description: str, photo: str, price: str, quantity: str, category_id: int, brand_id: int):
    """
    Добавляет новый продукт в базу данных.
    Проверяет на наличие дубликатов по имени.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        existing_product = db.query(Item).filter_by(name=name).first()
        if existing_product:
            return {'status': 0, 'message': 'Продукт уже существует'}
        new_product = Item(
            name=name,
            descr=description,
            photo=photo,
            price=price,
            count=quantity,
            category_id=category_id,
            brand_id=brand_id
        )
        db.add(new_product)
        db.commit()
        return {'status': 1, 'message': 'Продукт успешно создан'}

# Получение пользователя по ID
def get_user_by_id(user_id: int):
    """
    Возвращает пользователя из базы данных по его уникальному ID.
    Если пользователь не найден, возвращает сообщение об ошибке.
    """
    with next(get_db()) as db:
        user = db.query(Account).filter_by(id=user_id).first()
        if user:
            return user
        return {'status': 0, 'message': 'Пользователь не найден'}

# Удаление продукта по ID
def delete_product(product_id: int):
    """
    Удаляет продукт из базы данных по его уникальному ID.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return {'status': 1, 'message': 'Продукт успешно удален'}
        return {'status': 0, 'message': 'Продукт не найден'}

# Обновление данных продукта
def update_product(product_id: int, name: str = None, description: str = None, photo: str = None,
                   price: str = None, quantity: int = None, category_id: int = None, brand_id: int = None):
    """
    Обновляет информацию о продукте на основе предоставленных данных.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=product_id).first()
        if not product:
            return {'status': 0, 'message': 'Продукт не найден'}

        changes_made = False
        if name and name != 'string':
            product.name = name
            changes_made = True
        if description and description != 'string':
            product.descr = description
            changes_made = True
        if photo and photo != 'string':
            product.photo = photo
            changes_made = True
        if price and price != 'string':
            product.price = price
            changes_made = True
        if quantity and quantity != 'string':
            product.count = quantity
            changes_made = True
        if category_id and category_id != 0:
            product.category_id = category_id
            changes_made = True
        if brand_id and brand_id != 0:
            product.brand_id = brand_id
            changes_made = True

        if changes_made:
            db.commit()
            return {'status': 1, 'message': 'Продукт успешно обновлен'}
        return {'status': 0, 'message': 'Изменений не было сделано'}

# Обновление данных бренда
def update_brand(brand_id: int, name: str = None, description: str = None):
    """
    Обновляет данные бренда на основе предоставленных параметров.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        brand = db.query(ProductBrand).filter_by(id=brand_id).first()
        if not brand:
            return {'status': 0, 'message': 'Бренд не найден'}

        changes_made = False
        if name and name != 'string':
            brand.name = name
            changes_made = True
        if description and description != 'string':
            brand.descr = description
            changes_made = True

        if changes_made:
            db.commit()
            return {'status': 1, 'message': 'Бренд успешно обновлен'}
        return {'status': 0, 'message': 'Изменений не было сделано'}

# Удаление бренда по ID
def delete_brand(brand_id: int):
    """
    Удаляет бренд из базы данных по его уникальному ID.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        brand = db.query(ProductBrand).filter_by(id=brand_id).first()
        if brand:
            db.delete(brand)
            db.commit()
            return {'status': 1, 'message': 'Бренд успешно удален'}
        return {'status': 0, 'message': 'Бренд не найден'}

# Обновление данных категории
def update_category(category_id: int, name: str = None, description: str = None):
    """
    Обновляет данные категории на основе предоставленных параметров.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        category = db.query(ProductCategory).filter_by(id=category_id).first()
        if not category:
            return {'status': 0, 'message': 'Категория не найдена'}

        changes_made = False
        if name and name != 'string':
            category.name = name
            changes_made = True
        if description and description != 'string':
            category.descr = description
            changes_made = True

        if changes_made:
            db.commit()
            return {'status': 1, 'message': 'Категория успешно обновлена'}
        return {'status': 0, 'message': 'Изменений не было сделано'}

# Удаление категории по ID
def delete_category(category_id: int):
    """
    Удаляет категорию из базы данных по её уникальному ID.
    Возвращает сообщение о статусе операции.
    """
    with next(get_db()) as db:
        category = db.query(ProductCategory).filter_by(id=category_id).first()
        if category:
            db.delete(category)
            db.commit()
            return {'status': 1, 'message': 'Категория успешно удалена'}
        return {'status': 0, 'message': 'Категория не найдена'}
