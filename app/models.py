from sqlalchemy import Column, Integer, String, Float, ForeignKey
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
    tipo = Column(String)
    monto = Column(Float)
    socio_id = Column(Integer, ForeignKey("socios.id"))