from fastapi import FastAPI
from .database import engine, Base
from . import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Sistema de Gestión de Caja de Ahorros activo"}

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/socios/", response_model=schemas.SocioCreate)
def crear_socio(socio: schemas.SocioCreate, db: Session = Depends(get_db)):
    db_socio = models.Socio(**socio.dict())
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)
    return db_socio