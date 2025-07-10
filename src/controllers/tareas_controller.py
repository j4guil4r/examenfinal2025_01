from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.tarea import TareaCreate
from src.services import datahandler

router = APIRouter()

@router.post("/tasks")
def crear_tarea(request: TareaCreate, db: Session = Depends(get_db)):
    try:
        tarea_id = datahandler.crear_tarea(
            db,
            nombre=request.nombre,
            descripcion=request.descripcion,
            usuario=request.usuario,
            rol=request.rol
        )
        return {"tarea_id": tarea_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
