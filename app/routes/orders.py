"""Orders API routes for managing customer orders."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Create a new order with items and update product stock."""
    user = (
        db.query(models.User)
        .filter(models.User.id == order.user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    new_order = models.Order(user_id=order.user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.items:
        product = (
            db.query(models.Product)
            .filter(models.Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=400,
                detail=f"Producto ID {item.product_id} no encontrado"
            )

        current_stock = product.stock  # type: ignore
        if current_stock < item.quantity:  # type: ignore
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Stock insuficiente para el producto '{product.name}' "
                    f"(stock actual: {current_stock}, "
                    f"solicitado: {item.quantity})"
                )
            )

        # Descontar stock
        product.stock = current_stock - item.quantity  # type: ignore
        db.add(product)

        # Registrar en tabla intermedia
        stmt = models.order_product_table.insert().values(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity
        )
        db.execute(stmt)

    db.commit()
    db.refresh(new_order)

    # Recuperar productos con cantidades
    order_items = []
    for row in db.execute(
        models.order_product_table.select().where(
            models.order_product_table.c.order_id == new_order.id
        )
    ):
        product = db.query(models.Product).filter(
            models.Product.id == row.product_id
        ).first()
        order_items.append({
            "product": product,
            "quantity": row.quantity
        })

    return {
        "id": new_order.id,
        "user_id": new_order.user_id,
        "created_at": new_order.created_at,
        "items": order_items
    }


@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get an order by ID."""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order
