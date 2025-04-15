from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.reports_controller import router as reports_router

app = FastAPI()

# CORS abierto (puede ajustarse si necesitas restringir orígenes o métodos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reports_router)
