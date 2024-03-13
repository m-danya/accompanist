from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from accompanist.collection.router import router as collection_router
from accompanist.config import settings

app = FastAPI(
    title="Accompanist",
)

app.include_router(collection_router)

# TODO: use nginx to serve static files
app.mount("/static", StaticFiles(directory=settings.STORAGE_PATH), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
