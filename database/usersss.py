from database import get_db, Base
from database.models import Account, ProductCategory, ProductBrand, Item, ShoppingCart, Wishlist
from telebot import TeleBot
bot = TeleBot(token='7638142649:AAERr08pj68lsNoEvANk8Qzjyk9n5dC5Ufg')

def register_user(username: str, pass1: str, pass2: str, phone: str, mail: str = None, addr: str = None):
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

def authenticate_user(identifier: str, passwd: str):
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

def update_user_details(user_id: int, passwd: str, uname: str = None, phone: str = None, mail: str = None,
                        addr: str = None, new_pass: str = None):
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

def remove_user_account(user_id: int, passwd: str):
    with next(get_db()) as db:
        user = db.query(Account).filter_by(id=user_id).first()
        if user and user.password == passwd:
            db.delete(user)
            db.commit()
            return {'status': 1, 'message': 'Account deleted'}
        return {"status": 0, 'message': 'Error deleting account'}

def add_to_wishlist(user_id: int, product_id: int):
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

def remove_from_wishlist(user_id: int, product_id: int):
    with next(get_db()) as db:
        fav = db.query(Wishlist).filter_by(user_id=user_id, product_id=product_id).one_or_none()
        if fav:
            db.delete(fav)
            db.commit()
            return {'status': 1, 'message': 'Removed from wishlist'}
        return {'status': 0, 'message': 'Item not in wishlist'}

def add_to_shopping_cart(user_id: int, product_id: int, qty: int):
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

def remove_from_cart(user_id: int, product_id: int, qty: int):
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

def list_all_products():
    with next(get_db()) as db:
        return db.query(Item).all()

def filter_products_by_brand(brand_id: int):
    with next(get_db()) as db:
        return db.query(Item).filter_by(brand_id=brand_id).all()

def filter_products_by_category(cat_id: int):
    with next(get_db()) as db:
        return db.query(Item).filter_by(category_id=cat_id).all()

def list_all_categories():
    with next(get_db()) as db:
        return db.query(ProductCategory).all()

def list_all_brands():
    with next(get_db()) as db:
        return db.query(ProductBrand).all()

def get_product_details(prod_id: int):
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=prod_id).first()
        if product:
            return product
        return {'status': 0, 'message': 'Product not found'}

def get_brand_details(brand_id: int):
    with next(get_db()) as db:
        brand = db.query(ProductBrand).filter_by(id=brand_id).first()
        if brand:
            return brand
        return {'status': 0, 'message': 'Brand not found'}

def get_category_details(cat_id: int):
    with next(get_db()) as db:
        category = db.query(ProductCategory).filter_by(id=cat_id).first()
        if category:
            return category
        return {'status': 0, 'message': 'Category not found'}

def get_cart_details(cart_id: int):
    with next(get_db()) as db:
        cart = db.query(ShoppingCart).filter_by(id=cart_id).first()
        if cart:
            return cart
        return {'status': 0, 'message': 'Cart not found'}

def create_offer(prod_id: int, qty: int):
    with next(get_db()) as db:
        product = db.query(Item).filter_by(id=prod_id).first()
        return product
