from fastapi import FastAPI

from app.api import endpoints
from app.database.sharding import get_db_manager


app = FastAPI(title="Сократитель ссылок тестовый")


@app.on_event("startup")
async def on_startup():
    db_manager = get_db_manager()
    db_manager.create_all_tables()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(endpoints.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)