from sqlalchemy import Integer, Boolean, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship, validates
from database import get_db, Base
from datetime import datetime

class Account(Base):  # User -> Account
    __tablename__ = 'accounts'  # users -> accounts
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(30))
    password = Column(String)
    phone_number = Column(String, unique=True)
    email = Column(String, nullable=True, unique=True)
    address = Column(String, nullable=True)
    reg_date = Column(DateTime, default=datetime.now())
    cart_relationship = relationship('ShoppingCart', back_populates='account_relationship')  # cart_fk -> cart_relationship
    favorite_relationship = relationship('Wishlist', back_populates='account_relationship')  # fav_fk -> favorite_relationship

class ProductCategory(Base):  # Category -> ProductCategory
    __tablename__ = 'product_categories'  # categories -> product_categories
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String(2000))  # descr -> description
    created_at = Column(DateTime, default=datetime.now())

class ProductBrand(Base):  # Brand -> ProductBrand
    __tablename__ = 'product_brands'  # brands -> product_brands
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String(2000))  # descr -> description
    created_at = Column(DateTime, default=datetime.now())

class Item(Base):  # Product -> Item
    __tablename__ = 'items'  # products -> items
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    description = Column(String(2000), default='Описание товара')  # descr -> description
    image_url = Column(String, default='database/default_pics/istockphoto-1495088043-612x612.jpg')  # photo -> image_url
    price = Column(String)
    quantity = Column(Integer, default=0)  # count -> quantity
    category_id = Column(Integer, ForeignKey('product_categories.id'))
    brand_id = Column(Integer, ForeignKey('product_brands.id'))
    created_at = Column(DateTime, default=datetime.now())
    category_relationship = relationship(ProductCategory, lazy='subquery')  # category_fk -> category_relationship
    brand_relationship = relationship(ProductBrand, lazy='subquery')  # brand_fk -> brand_relationship

class ShoppingCart(Base):  # Cart -> ShoppingCart
    __tablename__ = 'shopping_carts'  # carts -> shopping_carts
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))  # user_id -> account_id
    item_id = Column(Integer, ForeignKey('items.id'))  # product_id -> item_id
    quantity = Column(Integer)  # count -> quantity
    created_at = Column(DateTime, default=datetime.now())
    account_relationship = relationship(Account, lazy='subquery', back_populates='cart_relationship')
    item_relationship = relationship(Item, lazy='subquery', passive_deletes=True)  # product_fk -> item_relationship

class Wishlist(Base):  # Favorite -> Wishlist
    __tablename__ = 'wishlists'  # favorites -> wishlists
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))  # user_id -> account_id
    item_id = Column(Integer, ForeignKey('items.id'))  # product_id -> item_id
    created_at = Column(DateTime, default=datetime.now())
    account_relationship = relationship(Account, lazy='subquery', back_populates='favorite_relationship')
    item_relationship = relationship(Item, lazy='subquery', passive_deletes=True)
