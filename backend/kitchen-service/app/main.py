from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.order_controller import router as order_controller
from app.controller.recipe_controller import router as recipe_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers para las órdenes y recetas
app.include_router(order_controller)
app.include_router(recipe_controller)

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass
