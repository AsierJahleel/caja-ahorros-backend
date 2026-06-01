from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Socio(Base):
    __tablename__ = "socios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    cedula = Column(String, unique=True)
    saldo = Column(Float, default=0.0)

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)  # "deposito" o "retiro"
    monto = Column(Float)