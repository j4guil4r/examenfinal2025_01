from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.database import Base

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, ForeignKey("tareas.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    rol = Column(String, nullable=False) 
    fecha_asignacion = Column(DateTime, default=datetime.now)

    # Relaciones bidireccionales
    tarea = relationship("Tarea", back_populates="usuarios_asignados")
    usuario = relationship("Usuario", back_populates="tareas_asociadas")
