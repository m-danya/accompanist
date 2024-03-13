from fastapi import APIRouter, status
from accompanist.collection.dao import AlbumDAO

from accompanist.collection.schema import AlbumInfoFromUser
from accompanist.collection import service


router = APIRouter(
    prefix="/collection",
    tags=["User's music collection"],
)


@router.post("/album", status_code=status.HTTP_202_ACCEPTED)
async def add_album(album_info: AlbumInfoFromUser):
    await service.add_album(album_info)


@router.get("/albums")
async def get_all_alumbs():
    albums = await AlbumDAO.get_all_with_tracks_and_artists()
    return albums
