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

@app.post("/transacciones/")
def crear_transaccion(tipo: str, monto: float, socio_id: int, db: Session = Depends(get_db)):
    socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    
    if tipo == "deposito":
        socio.saldo += monto
    elif tipo == "retiro":
        if socio.saldo < monto:
            raise HTTPException(status_code=400, detail="Fondos insuficientes")
        socio.saldo -= monto
    
    transaccion = models.Transaccion(tipo=tipo, monto=monto, socio_id=socio_id)
    db.add(transaccion)
    db.commit()
    return {"mensaje": "Transacción realizada con éxito", "nuevo_saldo": socio.saldo}# API Principal 
