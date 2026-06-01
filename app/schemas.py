from pydantic import BaseModel

class SocioCreate(BaseModel):
    nombre: str
    cedula: str
    saldo: float