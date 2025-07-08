"""Products API routes for managing products."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    """Create a new product."""
    category = (
        db.query(models.Category)
        .filter(models.Category.id == product.category_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=400, detail="Categoría no encontrada")
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    """Get all products."""
    return db.query(models.Product).all()
