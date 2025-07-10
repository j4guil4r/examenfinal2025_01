from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    alias = Column(String, unique=True, nullable=False)  # antes era "contacto"
    nombre = Column(String, nullable=False)

    tareas_asociadas = relationship("Asignacion", back_populates="usuario", cascade="all, delete-orphan")

    @property
    def tareas(self):
        return [asig.tarea for asig in self.tareas_asociadas if asig.tarea]