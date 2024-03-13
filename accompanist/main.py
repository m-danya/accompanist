from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from accompanist.collection.router import router as collection_router

app = FastAPI(
    title="Accompanist",
)

app.include_router(collection_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
