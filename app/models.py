"""Database models for the E-commerce application."""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Table
)
from sqlalchemy.orm import relationship
from app.database import Base

# Tabla intermedia para relación entre orden y productos
order_product_table = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("quantity", Integer, default=1),
)


class User(Base):
    """User model for authentication and orders."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="user")


class Category(Base):
    """Category model for product classification."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    products = relationship("Product", back_populates="category")


class Product(Base):
    """Product model for e-commerce items."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    orders = relationship(
        "Order",
        secondary=order_product_table,
        back_populates="products")


class Order(Base):
    """Order model for customer purchases."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    products = relationship(
        "Product",
        secondary=order_product_table,
        back_populates="orders")
