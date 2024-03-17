from fastapi import APIRouter, status
from loguru import logger

from accompanist.collection import service
from accompanist.collection.dao import AlbumDAO, TrackDAO
from accompanist.collection.schema import AlbumInfoFromUser

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


@router.post("/update_lyrics/{track_id}")
async def update_track_lyrics(track_id: int):
    await service.update_track_lyrics_by_id(track_id)


@router.post("/update_lyrics/")
async def update_all_tracks_lyrics():
    tracks = await TrackDAO.find_all()
    for i, track in enumerate(tracks):
        logger.info(f"Updating lyrics for track #{i}: {track.name}")
        try:
            await service.update_track_lyrics_by_id(track.id)
        except Exception:
            logger.error(f"Couldn't get lyrics for {track}, continuing..")
