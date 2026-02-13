from fastapi import FastAPI
from app.routes import endpoints

app = FastAPI()

app.include_router(endpoints.router)
