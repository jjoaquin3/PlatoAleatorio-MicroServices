from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import Database
from app.controller.ingredient_controller import router as ingredient_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredient_router)

@app.on_event("startup")
async def startup():
    # Ensure proper connection management using async with
    async with Database.get_engine().connect() as connection:
        # Optionally, you can perform some initial setup or checks here
        pass

@app.on_event("shutdown")
async def shutdown():
    # No need for explicit disconnection, SQLAlchemy handles connection pool
    await Database.get_engine().dispose()
