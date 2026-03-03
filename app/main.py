from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api import endpoints
from app.database.sharding import get_db_manager
from app.config.settings import get_settings


settings = get_settings()
app = FastAPI(title=settings.app_title)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(endpoints.router)


@app.get("/")
async def serve_frontend():
    return FileResponse(settings.index_page)


app.mount("/", StaticFiles(directory=str(settings.frontend_directory)), name="static")


@app.on_event("startup")
async def on_startup():
    db_manager = get_db_manager()
    await db_manager.create_all_tables()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)