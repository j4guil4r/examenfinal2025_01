from pydantic import BaseModel
from typing import List, Optional
from src.schemas.tarea import TareaOut

class UsuarioBase(BaseModel):
    alias: str
    nombre: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: int
    tareas: List[TareaOut] = []

    class Config:
        orm_mode = True
