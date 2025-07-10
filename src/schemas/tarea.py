from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.schemas.asignacion import AsignacionOut  

class TareaBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_esperada_fin: Optional[datetime] = None

class TareaCreate(TareaBase):
    usuario: str  
    rol: str  

class TareaEstadoUpdate(BaseModel):
    estado: str  

class TareaOut(TareaBase):
    id: str
    estado: str
    usuarios_asignados: List[AsignacionOut] = []

    class Config:
        orm_mode = True

