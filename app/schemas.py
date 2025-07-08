"""Pydantic schemas for the E-commerce API."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


class UserOut(UserBase):
    """Schema for user output."""
    id: int
    is_active: bool

    class Config:
        """Pydantic configuration for ORM mode."""
        orm_mode = True


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""


class CategoryOut(CategoryBase):
    """Schema for category output."""
    id: int

    class Config:
        """Pydantic configuration for ORM mode."""
        orm_mode = True


class ProductBase(BaseModel):
    """Base product schema."""
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int


class ProductCreate(ProductBase):
    """Schema for creating a product."""


class ProductOut(ProductBase):
    """Schema for product output."""
    id: int
    category: CategoryOut

    class Config:
        """Pydantic configuration for ORM mode."""
        orm_mode = True


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item."""


class OrderItemOut(BaseModel):
    """Schema for order item output."""
    product: ProductOut
    quantity: int

    class Config:
        """Pydantic configuration for ORM mode."""
        orm_mode = True


class OrderBase(BaseModel):
    """Base order schema."""
    user_id: int


class OrderCreate(OrderBase):
    """Schema for creating an order."""
    items: List[OrderItemCreate]


class OrderOut(OrderBase):
    """Schema for order output."""
    id: int
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        """Pydantic configuration for ORM mode."""
        orm_mode = True
