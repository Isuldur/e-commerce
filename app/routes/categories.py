"""Categories API routes for managing product categories."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db


router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=schemas.CategoryOut)
def create_category(
    category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    """Create a new category."""
    db_category = (
        db.query(models.Category)
        .filter(models.Category.name == category.name)
        .first()
    )
    if db_category:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """Get all categories."""
    return db.query(models.Category).all()
