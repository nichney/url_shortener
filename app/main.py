from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api import endpoints
from app.database.sharding import get_db_manager


app = FastAPI(title="Сократитель ссылок")

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.on_event("startup")
async def on_startup():
    db_manager = get_db_manager()
    db_manager.create_all_tables()


@app.get("/")
async def read_root():
    # Отдаем index.html из папки frontend
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(endpoints.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)