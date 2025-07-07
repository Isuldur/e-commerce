# app/main.py
from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI(title="E-commerce API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"msg": "Bienvenido a la API de E-commerce"}
