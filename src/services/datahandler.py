from sqlalchemy.orm import Session
from datetime import datetime

from src.models.usuario import Usuario
from src.models.tarea import Tarea
from src.models.asignacion import Asignacion
from src.models.dependencia import Dependencia
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload


# Crear usuario
def crear_usuario(db: Session, alias: str, nombre: str):
    if db.query(Usuario).filter_by(alias=alias).first():
        raise HTTPException(status_code=422, detail="Alias ya existe")
    usuario = Usuario(alias=alias, nombre=nombre)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# Obtener usuario con sus tareas
def obtener_usuario_con_tareas(db: Session, alias: str):
    usuario = db.query(Usuario)\
        .options(joinedload(Usuario.tareas_asociadas).joinedload(Asignacion.tarea))\
        .filter_by(alias=alias)\
        .first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario


# Crear tarea y asignar usuario inicial
def crear_tarea(db: Session, nombre: str, descripcion: str, usuario: str, rol: str):
    user = db.query(Usuario).filter_by(alias=usuario).first()
    if not user:
        raise ValueError("Usuario no encontrado")

    tarea_id = str(uuid.uuid4())
    nueva_tarea = Tarea(
        id=tarea_id,
        nombre=nombre,
        description=descripcion,
        fecha_esperada_fin=datetime.now(), 
    )
    db.add(nueva_tarea)
    db.flush()  

    asignacion = Asignacion(
        task_id=tarea_id,
        user_id=user.id,
        rol=rol
    )
    db.add(asignacion)
    db.commit()
    return tarea_id


# Cambiar estado de la tarea
def actualizar_estado_tarea(db: Session, tarea_id: str, nuevo_estado: str):
    tarea = db.query(Tarea).filter_by(id=tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    transiciones_validas = {
        "nueva": ["enprogreso"],
        "enprogreso": ["finalizada", "nueva"]
    }

    if tarea.estado == "finalizada":
        raise HTTPException(status_code=422, detail="No se puede cambiar el estado de una tarea finalizada")

    if nuevo_estado not in transiciones_validas.get(tarea.estado, []):
        raise HTTPException(status_code=422, detail=f"Transición inválida desde {tarea.estado} a {nuevo_estado}")

    # Validar dependencias si va a finalizar
    if nuevo_estado == "finalizada":
        for dep in tarea.dependencias:
            if dep.depende_de.estado != "finalizada":
                raise HTTPException(status_code=422, detail="No se puede finalizar, dependencias incompletas")

    tarea.estado = nuevo_estado
    db.commit()
    return tarea


# Asignar o remover usuario
def modificar_usuario_en_tarea(db: Session, tarea_id: str, alias_usuario: str, rol: str, accion: str):
    tarea = db.query(Tarea).filter_by(id=tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    usuario = db.query(Usuario).filter_by(alias=alias_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    asignacion = db.query(Asignacion).filter_by(user_id=usuario.id, task_id=tarea.id).first()

    if accion == "adicionar":
        if asignacion:
            raise HTTPException(status_code=422, detail="Usuario ya asignado")
        nueva = Asignacion(user_id=usuario.id, task_id=tarea.id, rol=rol, fecha_asignacion=datetime.now())
        db.add(nueva)
        db.commit()
    elif accion == "remover":
        if not asignacion:
            raise HTTPException(status_code=422, detail="Usuario no asignado")
        db.delete(asignacion)
        db.commit()

    # Validar que quede al menos un usuario
    if not db.query(Asignacion).filter_by(task_id=tarea.id).first():
        raise HTTPException(status_code=422, detail="La tarea debe tener al menos un usuario asignado")



# Agregar o remover dependencia
def modificar_dependencia(db: Session, tarea_id: str, depende_de_id: str, accion: str):
    tarea = db.query(Tarea).filter_by(id=tarea_id).first()
    dependencia = db.query(Tarea).filter_by(id=depende_de_id).first()

    if not tarea or not dependencia:
        raise HTTPException(status_code=404, detail="Tarea o dependencia no encontrada")

    existente = db.query(Dependencia).filter_by(tarea_id=tarea_id, depende_de_id=depende_de_id).first()

    if accion == "adicionar":
        if existente:
            raise HTTPException(status_code=422, detail="Ya existe la dependencia")
        nueva = Dependencia(tarea_id=tarea_id, depende_de_id=depende_de_id)
        db.add(nueva)
        db.commit()
    elif accion == "remover":
        if not existente:
            raise HTTPException(status_code=422, detail="La dependencia no existe")
        db.delete(existente)
        db.commit()
