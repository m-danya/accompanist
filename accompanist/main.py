from fastapi import FastAPI

from accompanist.collection.router import router as collection_router

app = FastAPI(
    title="Accompanist",
)

app.include_router(collection_router)
