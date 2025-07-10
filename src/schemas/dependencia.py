from pydantic import BaseModel

class DependenciaBase(BaseModel):
    dependencytaskid: str
    accion: str

class DependenciaOut(BaseModel):
    id: int
    tarea_id: str
    depende_de_id: str

    class Config:
        orm_mode = True
