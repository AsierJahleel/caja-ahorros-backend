from fastapi import FastAPI
from .database import engine, Base
from . import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Sistema de Gestión de Caja de Ahorros activo"}