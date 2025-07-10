from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas.usuario import UsuarioCreate, UsuarioOut
from src.services import datahandler
from src.db.database import get_db

router = APIRouter()

@router.post("", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return datahandler.crear_usuario(db, alias=usuario.alias, nombre=usuario.nombre)

@router.get("/mialias={alias}", response_model=UsuarioOut)
def obtener_usuario(alias: str, db: Session = Depends(get_db)):
    return datahandler.obtener_usuario_con_tareas(db, alias)

