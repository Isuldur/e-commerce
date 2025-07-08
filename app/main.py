from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes import categories, products, users, orders

app = FastAPI(title="E-commerce API")

Base.metadata.create_all(bind=engine)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"msg": "API de E-commerce funcionando"}
