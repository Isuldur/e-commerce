"""Tests for orders API endpoints."""
import sys
import os
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import User, Product, Category
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )


client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Set up test database with sample data."""
    # Crea tablas
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Crea un usuario
    user = User(
        username="cliente1",
        email="cliente1@example.com",
        hashed_password="hashed123"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Crea categoría y producto
    category = Category(name="Electrónica")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Audífonos",
        description="Audífonos inalámbricos",
        price=500.0,
        stock=10,
        category_id=category.id
    )
    db.add(product)
    db.commit()
    db.close()

    yield
    # Limpieza final
    Base.metadata.drop_all(bind=engine)


def test_create_valid_order():
    """Test creating a valid order with sufficient stock."""
    db = SessionLocal()
    user = db.query(User).first()
    product = db.query(Product).first()
    db.close()
    assert user is not None
    assert product is not None

    response = client.post("/orders/", json={
        "user_id": user.id,
        "items": [
            {
                "product_id": product.id,
                "quantity": 2
            }
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user.id
    assert data["items"][0]["product"]["name"] == "Audífonos"
    assert data["items"][0]["quantity"] == 2


def test_create_order_insufficient_stock():
    """Test creating an order with insufficient stock."""
    db = SessionLocal()
    user = db.query(User).first()
    product = db.query(Product).first()
    db.close()
    assert user is not None
    assert product is not None

    response = client.post("/orders/", json={
        "user_id": user.id,
        "items": [
            {
                "product_id": product.id,
                "quantity": 999  # más de lo disponible
            }
        ]
    })

    assert response.status_code == 400
    assert "Stock insuficiente" in response.text
