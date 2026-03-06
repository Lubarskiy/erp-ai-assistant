from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.router import api_router
from app.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(api_router, prefix=settings.api_prefix)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/templates"), name="static")

@app.get("/")
def root():
    return {"status": "running", "app": settings.app_name}

@app.get("/health")
def health():
    return {"ok": True}
