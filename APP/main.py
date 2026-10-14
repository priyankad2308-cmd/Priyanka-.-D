from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from APP.routes import router

app = FastAPI(
    title="ComicCraft AI",
    version="1.0.0"
)

# Static files
app.mount("/static", StaticFiles(directory="APP/static"), name="static")

# Routes
app.include_router(router)
