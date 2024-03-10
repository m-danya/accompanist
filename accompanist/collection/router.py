from fastapi import APIRouter


router = APIRouter(
    prefix="/collection",
    tags=["User's music collection"],
)


@router.get("/song")
async def get_song():
    return "some song"
