from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from src.db.database import Base
import enum

class EstadoTarea(str, enum.Enum):
    nueva = "nueva"
    enprogreso = "enprogreso"
    finalizada = "finalizada"

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    estado = Column(Enum(EstadoTarea), default=EstadoTarea.nueva, nullable=False)
    fecha_esperada_fin = Column(DateTime, nullable=False)

    usuarios_asignados = relationship(
        "Asignacion",
        back_populates="tarea",
        cascade="all, delete-orphan"
    )

    dependencias = relationship(
        "Dependencia",
        foreign_keys="Dependencia.tarea_id",
        back_populates="tarea",
        cascade="all, delete-orphan"
    )

    dependientes_de = relationship(
        "Dependencia",
        foreign_keys="Dependencia.depende_de_id",
        back_populates="depende_de",
        cascade="all, delete-orphan"
    )
