from fastapi import FastAPI
from src.config.settings import settings
from src.db.database import init_db
from src.controllers import usuarios_controller, tareas_controller

app = FastAPI(
    title="App Examen Final",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(usuarios_controller.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(tareas_controller.router, prefix="/tasks", tags=["tasks"])