from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.controller.flow_controller import router as flow_router
from app.config.redis_client import RedisClient
from app.controller.debug_controller import router as debug_router

app = FastAPI()

# CORS abierto (puede ajustarse si necesitás)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas principales del orquestador
app.include_router(flow_router)
app.include_router(debug_router)

@app.on_event("startup")
def startup_event():
    try:
        RedisClient.get_client()  # Fuerza la conexión al levantar
    except Exception as e:
        print(f"💥 Error al conectar a Redis: {e}")
        raise

@app.on_event("shutdown")
def shutdown_event():
    try:
        RedisClient.close()  # Fuerza cierra de conexión
    except Exception as e:
        print(f"💥 Error al cerrar conexión Redis: {e}")