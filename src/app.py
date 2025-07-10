from fastapi import FastAPI
from src.config.settings import settings
from src.db.database import init_db
from src.controllers import usuarios_controller

app = FastAPI(
    title="Microservicio de Cursos",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(usuarios_controller.router, prefix="/usuarios", tags=["usuarios"])
#app.include_router(inscripciones.router, prefix="/inscripciones", tags=["inscripciones"])