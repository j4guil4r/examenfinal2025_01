from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class Dependencia(Base):
    __tablename__ = "dependencias"

    id = Column(Integer, primary_key=True)
    tarea_id = Column(String, ForeignKey("tareas.id"), nullable=False)
    depende_de_id = Column(String, ForeignKey("tareas.id"), nullable=False)

    tarea = relationship(
        "Tarea",
        foreign_keys=[tarea_id],
        back_populates="dependencias"
    )

    depende_de = relationship(
        "Tarea",
        foreign_keys=[depende_de_id],
        back_populates="dependientes_de"
    )
