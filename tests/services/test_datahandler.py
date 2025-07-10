import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime

from src.services.datahandler import (
    crear_usuario,
    obtener_usuario_con_tareas,
    crear_tarea,
    actualizar_estado_tarea,
    modificar_usuario_en_tarea,
    modificar_dependencia
)
from src.models.usuario import Usuario
from src.models.tarea import Tarea
from src.models.asignacion import Asignacion
from src.models.dependencia import Dependencia


# creacion de los usuarios
def test_crear_usuario_exitoso():
    db = MagicMock()
    db.query().filter_by().first.return_value = None
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    result = crear_usuario(db, "nuevo_alias", "Nombre")
    assert result.alias == "nuevo_alias"
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_crear_usuario_alias_existente():
    db = MagicMock()
    db.query().filter_by().first.return_value = Usuario(alias="existe")
    with pytest.raises(HTTPException) as exc:
        crear_usuario(db, "existe", "Nombre")
    assert exc.value.status_code == 422


# obtener usuarios con sus tareas
def test_obtener_usuario_con_tareas_existe():
    usuario = Usuario(alias="usuario1")
    db = MagicMock()
    db.query().filter_by().first.return_value = usuario
    result = obtener_usuario_con_tareas(db, "usuario1")
    assert result.alias == "usuario1"

def test_obtener_usuario_con_tareas_no_existe():
    db = MagicMock()
    db.query().filter_by().first.return_value = None
    with pytest.raises(HTTPException) as exc:
        obtener_usuario_con_tareas(db, "noexiste")
    assert exc.value.status_code == 404


# lacrecaion de una tarea
def test_crear_tarea_exito():
    usuario = Usuario(id=1, alias="u1")
    db = MagicMock()
    db.query().filter_by().first.return_value = usuario
    db.add = MagicMock()
    db.flush = MagicMock()
    db.commit = MagicMock()
    tarea_id = crear_tarea(db, "tareaX", "desc", "u1", "rolX")
    assert isinstance(tarea_id, str)

def test_crear_tarea_usuario_no_encontrado():
    db = MagicMock()
    db.query().filter_by().first.return_value = None
    with pytest.raises(ValueError):
        crear_tarea(db, "tarea", "desc", "missing", "rol")


# actualizar estado de las tareas en general
def test_actualizar_estado_valida():
    tarea = Tarea(id="1", estado="nueva", dependencias=[])
    db = MagicMock()
    db.query().filter_by().first.return_value = tarea
    db.commit = MagicMock()
    result = actualizar_estado_tarea(db, "1", "enprogreso")
    assert result.estado == "enprogreso"

def test_actualizar_estado_tarea_no_encontrada():
    db = MagicMock()
    db.query().filter_by().first.return_value = None
    with pytest.raises(HTTPException) as exc:
        actualizar_estado_tarea(db, "x", "enprogreso")
    assert exc.value.status_code == 404

def test_actualizar_estado_tarea_finalizada():
    tarea = Tarea(id="1", estado="finalizada")
    db = MagicMock()
    db.query().filter_by().first.return_value = tarea
    with pytest.raises(HTTPException) as exc:
        actualizar_estado_tarea(db, "1", "nueva")
    assert exc.value.status_code == 422

def test_actualizar_estado_transicion_invalida():
    tarea = Tarea(id="1", estado="nueva")
    db = MagicMock()
    db.query().filter_by().first.return_value = tarea
    with pytest.raises(HTTPException) as exc:
        actualizar_estado_tarea(db, "1", "finalizada")
    assert exc.value.status_code == 422

def test_actualizar_estado_dependencias_incompletas():
    dep = MagicMock()
    dep.depende_de.estado = "enprogreso"
    tarea = Tarea(id="1", estado="enprogreso", dependencias=[dep])
    db = MagicMock()
    db.query().filter_by().first.return_value = tarea
    with pytest.raises(HTTPException) as exc:
        actualizar_estado_tarea(db, "1", "finalizada")
    assert exc.value.status_code == 422


# modificaciones de usuarios en las tareas
def test_modificar_usuario_adicionar():
    tarea = Tarea(id="1")
    usuario = Usuario(id=2, alias="x")
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, usuario, None, MagicMock()]
    db.commit = MagicMock()
    modificar_usuario_en_tarea(db, "1", "x", "rol", "adicionar")
    db.add.assert_called_once()

def test_modificar_usuario_remover():
    tarea = Tarea(id="1")
    usuario = Usuario(id=2, alias="x")
    asignacion = MagicMock()
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, usuario, asignacion, MagicMock()]
    db.commit = MagicMock()
    modificar_usuario_en_tarea(db, "1", "x", "rol", "remover")
    db.delete.assert_called_once()

def test_modificar_usuario_no_encontrado():
    tarea = Tarea(id="1")
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, None]
    with pytest.raises(HTTPException) as exc:
        modificar_usuario_en_tarea(db, "1", "noexiste", "rol", "adicionar")
    assert exc.value.status_code == 404

def test_modificar_usuario_deja_vacia():
    tarea = Tarea(id="1")
    usuario = Usuario(id=2)
    asignacion = MagicMock()
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, usuario, asignacion, None]
    db.commit = MagicMock()
    with pytest.raises(HTTPException) as exc:
        modificar_usuario_en_tarea(db, "1", "x", "rol", "remover")
    assert exc.value.status_code == 422

#cubrir caso donde intenta remover y el usuario no está asignado
def test_modificar_usuario_remover_no_asignado():
    tarea = Tarea(id="1")
    usuario = Usuario(id=2)
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, usuario, None]
    with pytest.raises(HTTPException) as exc:
        modificar_usuario_en_tarea(db, "1", "x", "rol", "remover")
    assert exc.value.status_code == 422


# Modificaciones a la dependencia
def test_modificar_dependencia_adicionar():
    tarea = Tarea(id="1")
    depende = Tarea(id="2")
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, depende, None]
    modificar_dependencia(db, "1", "2", "adicionar")
    db.add.assert_called_once()

def test_modificar_dependencia_remover():
    tarea = Tarea(id="1")
    depende = Tarea(id="2")
    existente = MagicMock()
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, depende, existente]
    modificar_dependencia(db, "1", "2", "remover")
    db.delete.assert_called_once()

def test_modificar_dependencia_no_encontrada():
    db = MagicMock()
    db.query().filter_by().first.side_effect = [None, None]
    with pytest.raises(HTTPException) as exc:
        modificar_dependencia(db, "1", "2", "adicionar")
    assert exc.value.status_code == 404

#cubrir caso donde intenta remover una dependencia que no existe
def test_modificar_dependencia_remover_no_existente():
    tarea = Tarea(id="1")
    depende = Tarea(id="2")
    db = MagicMock()
    db.query().filter_by().first.side_effect = [tarea, depende, None]
    with pytest.raises(HTTPException) as exc:
        modificar_dependencia(db, "1", "2", "remover")
    assert exc.value.status_code == 422
