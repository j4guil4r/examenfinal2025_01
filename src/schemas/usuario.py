from pydantic import BaseModel
from typing import List, Optional

class UsuarioBase(BaseModel):
    alias: str
    nombre: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
