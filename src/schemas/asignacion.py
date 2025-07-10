from pydantic import BaseModel
from datetime import datetime

class AsignacionBase(BaseModel):
    usuario: str  
    rol: str
    accion: str  

class AsignacionCreate(AsignacionBase):
    pass

class AsignacionOut(BaseModel):
    user_id: int
    rol: str
    fecha_asignacion: datetime

    class Config:
        orm_mode = True
