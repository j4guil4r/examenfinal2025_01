import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime

from src.services import datahandler
from src.models.usuario import Usuario
from src.models.tarea import Tarea
from src.models.asignacion import Asignacion


# Caso de éxito: crear usuario nuevo
def test_crear_usuario_exitoso():
    db = MagicMock()
    db.query().filter_by().first.return_value = None  

    nuevo = Usuario(alias="juan", nombre="Juan Perez")
    db.add.side_effect = lambda u: setattr(u, "id", 1)
    db.commit.return_value = None
    db.refresh.side_effect = lambda u: None

    result = datahandler.crear_usuario(db, "juan", "Juan Perez")

    assert isinstance(result, Usuario)
    assert result.alias == "juan"
    assert db.add.called
    assert db.commit.called


# Error: alias ya existe
def test_crear_usuario_alias_existente():
    db = MagicMock()
    db.query().filter_by().first.return_value = Usuario(alias="juan")

    with pytest.raises(HTTPException) as e:
        datahandler.crear_usuario(db, "juan", "Otro Nombre")

    assert e.value.status_code == 422
    assert "Alias ya existe" in str(e.value.detail)


# Error: usuario no encontrado al crear tarea
def test_crear_tarea_usuario_inexistente():
    db = MagicMock()
    db.query().filter_by().first.return_value = None

    with pytest.raises(ValueError) as e:
        datahandler.crear_tarea(db, "Tarea 1", "Desc", "no_existe", "admin")

    assert "Usuario no encontrado" in str(e.value)


# Error: obtener usuario que no existe
def test_obtener_usuario_con_tareas_inexistente():
    db = MagicMock()
    db.query().filter_by().first.return_value = None

    with pytest.raises(HTTPException) as e:
        datahandler.obtener_usuario_con_tareas(db, "fantasma")

    assert e.value.status_code == 404
    assert "Usuario no encontrado" in str(e.value.detail)
