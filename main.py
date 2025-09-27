from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import attempt_routes, record_routes
from database.database import test_connection
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio (startup)
    await test_connection()
    yield
    # Evento de cierre (shutdown)
    print("Cerrando la aplicación...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(attempt_routes.router, prefix="/attempts", tags=["Attempts"])
app.include_router(record_routes.router, prefix="/records", tags=["Records"])
