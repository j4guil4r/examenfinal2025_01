from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.tarea import TareaCreate
from src.services import datahandler
from src.schemas.tarea import TareaEstadoUpdate
from src.schemas.dependencia import DependenciaBase

router = APIRouter()

@router.post("")
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
    

@router.post("/{id}")
def cambiar_estado_tarea(id: str, payload: TareaEstadoUpdate, db: Session = Depends(get_db)):
    tarea = datahandler.actualizar_estado_tarea(db, tarea_id=id, nuevo_estado=payload.estado)
    return {"id": tarea.id, "estado": tarea.estado}

from src.schemas.asignacion import AsignacionCreate

@router.post("/{id}/users")
def modificar_usuario_tarea(id: str, asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    datahandler.modificar_usuario_en_tarea(
        db=db,
        tarea_id=id,
        alias_usuario=asignacion.usuario,
        rol=asignacion.rol,
        accion=asignacion.accion
    )
    return {"detail": "Operación realizada correctamente"}

@router.post("/{id}/dependencies")
def modificar_dependencia_tarea(id: str, dependencia: DependenciaBase, db: Session = Depends(get_db)):
    datahandler.modificar_dependencia(
        db=db,
        tarea_id=id,
        depende_de_id=dependencia.dependencytaskid,
        accion=dependencia.accion
    )
    return {"detail": "Operación realizada correctamente"}


