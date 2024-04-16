from fastapi import APIRouter, status
from loguru import logger

from accompanist.collection import service
from accompanist.collection.dao import AlbumDAO, TrackDAO
from accompanist.collection.schema import (
    AlbumInfoFromUser,
    TrackUpdateRequest,
)
from accompanist.exceptions import TrackNotFoundException

router = APIRouter(
    tags=["User's music collection"],
)


@router.post("/album", status_code=status.HTTP_202_ACCEPTED)
async def add_album(album_info: AlbumInfoFromUser):
    await service.add_album(album_info)


@router.get("/album/{album_id}")
async def get_album(album_id: int):
    album = await AlbumDAO.get_by_id_with_tracks_info(album_id)
    return album


@router.delete("/album/{album_id}")
async def delete_album(album_id: int):
    await AlbumDAO.delete(id=album_id)


@router.get("/albums")
async def get_all_alumbs():
    albums = await AlbumDAO.get_all()
    return albums


@router.get("/track/{track_id}")
async def get_track(track_id: int):
    track = await TrackDAO.find_one_or_none(id=track_id)
    if not track:
        raise TrackNotFoundException(id=track_id)
    return track


@router.patch("/track/{track_id}")
async def update_track(track_id: int, update_request: TrackUpdateRequest):
    updated_track = await TrackDAO.update(track_id, update_request)
    return updated_track


@router.post("/tracks/{track_id}/lyrics")
async def update_track_lyrics(track_id: int):
    track = await service.update_track_lyrics_by_id(track_id)
    return track


@router.post("/update_lyrics_dev", include_in_schema=False)
async def update_all_tracks_lyrics():
    tracks = await TrackDAO.find_all()
    for i, track in enumerate(tracks):
        logger.info(f"Updating lyrics for track #{i}: {track.name}")
        try:
            await service.update_track_lyrics_by_id(track.id)
        except Exception:
            logger.error(f"Couldn't get lyrics for {track}, continuing..")
