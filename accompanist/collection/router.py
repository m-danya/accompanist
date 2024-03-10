from fastapi import APIRouter

from accompanist.collection.schema import AlbumInfoFromUser
from accompanist.collection import service


router = APIRouter(
    prefix="/collection",
    tags=["User's music collection"],
)


@router.post("/album")
async def add_album(album_info: AlbumInfoFromUser):
    album = await service.add_album(album_info)
    return album
