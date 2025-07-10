from sqlalchemy import Column, String, DateTime, Enum, Integer
from sqlalchemy.orm import relationship
from src.db.database import Base
import enum
from datetime import datetime

class EstadoTarea(str, enum.Enum):
    nueva = "nueva"
    emprogreso = "enprogreso"
    finalizada = "finalizada"

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(String, primary_key=True)  
    nombre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    estado = Column(Enum(EstadoTarea), default=EstadoTarea.nueva, nullable=False)
    fecha_esperada_fin = Column(DateTime, nullable=False)

    usuarios_asignados = relationship("Asignacion", back_populates="tarea", cascade="all, delete-orphan")
    dependencias = relationship("Dependencia", back_populates="tarea", cascade="all, delete-orphan")