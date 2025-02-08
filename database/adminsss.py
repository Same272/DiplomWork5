from database import get_db, Base
from database.models import Account, ProductCategory, ProductBrand, Item, ShoppingCart, Wishlist

def create_category(name: str, description: str):
    with next(get_db()) as db:
        existing_category = db.query(ProductCategory).filter_by(name=name).first()
        if existing_category:
            return {'status': 0, 'message': 'Category already exists'}
        new_category = ProductCategory(name=name, descr=description)
        db.add(new_category)
        db.commit()
        return {'status': 1, 'message': 'Category created successfully'}

def create_brand(name: str, description: str):
    with next(get_db()) as db:
        existing_brand = db.query(ProductBrand).filter_by(name=name).first()
        if existing_brand:
            return {'status': 0, 'message': 'Brand already exists'}
        new_brand = ProductBrand(name=name, descr=description)
        db.add(new_brand)
        db.commit()
        return {'status': 1, 'message': 'Brand created successfully'}

def create_product(name: str, description: str, photo: str, price: str, quantity: str, category_id: int, brand_id: int):
    with next(get_db()) as db:
        existing_product = db.query(Item).filter_by(name=name).first()
        if existing_product:
            return {'status': 0, 'message': 'Product already exists'}
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
        return {'status': 1, 'message': 'Product created successfully'}

def get_user_by_id(user_id: int):
    with next(get_db()) as db:
        user = db.query(Account).filter_by(id=user_id).first()
        if user:
            return user
        return {'status': 0, 'message': 'User not found'}

def delete_product(product_id: int):
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return {'status': 1, 'message': 'Product deleted successfully'}
        return {'status': 0, 'message': 'Product not found'}

def update_product(product_id: int, name: str = None, description: str = None, photo: str = None,
                   price: str = None, quantity: int = None, category_id: int = None, brand_id: int = None):
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=product_id).first()
        if not product:
            return {'status': 0, 'message': 'Product not found'}

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
            return {'status': 1, 'message': 'Product updated successfully'}
        return {'status': 0, 'message': 'No changes were made'}

def update_brand(brand_id: int, name: str = None, description: str = None):
    with next(get_db()) as db:
        brand = db.query(ProductBrand).filter_by(id=brand_id).first()
        if not brand:
            return {'status': 0, 'message': 'Brand not found'}

        changes_made = False
        if name and name != 'string':
            brand.name = name
            changes_made = True
        if description and description != 'string':
            brand.descr = description
            changes_made = True

        if changes_made:
            db.commit()
            return {'status': 1, 'message': 'Brand updated successfully'}
        return {'status': 0, 'message': 'No changes were made'}

def delete_brand(brand_id: int):
    with next(get_db()) as db:
        brand = db.query(ProductBrand).filter_by(id=brand_id).first()
        if brand:
            db.delete(brand)
            db.commit()
            return {'status': 1, 'message': 'Brand deleted successfully'}
        return {'status': 0, 'message': 'Brand not found'}

def update_category(category_id: int, name: str = None, description: str = None):
    with next(get_db()) as db:
        category = db.query(ProductCategory).filter_by(id=category_id).first()
        if not category:
            return {'status': 0, 'message': 'Category not found'}

        changes_made = False
        if name and name != 'string':
            category.name = name
            changes_made = True
        if description and description != 'string':
            category.descr = description
            changes_made = True

        if changes_made:
            db.commit()
            return {'status': 1, 'message': 'Category updated successfully'}
        return {'status': 0, 'message': 'No changes were made'}

def delete_category(category_id: int):
    with next(get_db()) as db:
        category = db.query(ProductCategory).filter_by(id=category_id).first()
        if category:
            db.delete(category)
            db.commit()
            return {'status': 1, 'message': 'Category deleted successfully'}
        return {'status': 0, 'message': 'Category not found'}
