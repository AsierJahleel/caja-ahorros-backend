"""from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from . import models, schemas

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"mensaje": "Sistema de Gestión de Caja de Ahorros activo"}

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
    return {"mensaje": "Transacción realizada con éxito", "nuevo_saldo": socio.saldo}

# Fin de la API Principal //
######"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import engine, Base, SessionLocal
from . import models

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Caja de Ahorros",
    description="Backend para la gestión de socios y transacciones contables",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ESQUEMAS PYDANTIC ---
class SocioCreate(BaseModel):
    nombre: str
    cedula: str
    saldo: float = 0.0

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"mensaje": "Sistema de Gestión de Caja de Ahorros activo"}

@app.get("/socios/")
def listar_socios(db: Session = Depends(get_db)):
    return db.query(models.Socio).all()

@app.post("/socios/", status_code=status.HTTP_201_CREATED)
def crear_socio(socio: SocioCreate, db: Session = Depends(get_db)):
    socio_existente = db.query(models.Socio).filter(models.Socio.cedula == socio.cedula).first()
    if socio_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La cédula '{socio.cedula}' ya se encuentra registrada en el sistema."
        )
    
    db_socio = models.Socio(
        nombre=socio.nombre,
        cedula=socio.cedula,
        saldo=socio.saldo
    )
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)
    return db_socio

@app.post("/transacciones/")
def crear_transaccion(tipo: str, monto: float, socio_id: int, db: Session = Depends(get_db)):
    # 1. Verificar si el socio existe en la base de datos
    socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()
    if not socio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Socio no encontrado"
        )
    
    tipo_norm = tipo.lower().strip()
    
    # 2. Validar el tipo de operación y actualizar la entidad del socio
    if tipo_norm in ["deposito", "depósito"]:
        socio.saldo += monto
    elif tipo_norm == "retiro":
        if socio.saldo < monto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Fondos insuficientes para realizar el retiro"
            )
        socio.saldo -= monto
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de transacción no válido. Use 'deposito' o 'retiro'."
        )
    
    # 3. Registrar la transacción coincidiendo exactamente con la clase Transaccion
    try:
        nueva_transaccion = models.Transaccion(
            tipo=tipo_norm,
            monto=monto,
            socio_id=socio_id
        )
        db.add(nueva_transaccion)
        db.commit()
        db.refresh(socio)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar la transacción en BD: {str(e)}"
        )
    
    return {
        "mensaje": "Transacción realizada con éxito", 
        "socio_id": socio.id,
        "nuevo_saldo": socio.saldo
    }

@app.get("/transacciones/")
def listar_transacciones(db: Session = Depends(get_db)):

    transacciones = db.query(models.Transaccion).all()

    return transacciones