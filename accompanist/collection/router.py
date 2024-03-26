from fastapi import APIRouter, status
from loguru import logger

from accompanist.collection import service
from accompanist.collection.dao import AlbumDAO, TrackDAO
from accompanist.collection.schema import (
    AlbumInfoFromUser,
    IsFavoriteFromUser,
    LyricsKaraokeFromUser,
)

router = APIRouter(
    prefix="/collection",
    tags=["User's music collection"],
)

# TODO [!!!]: refactor endpoint paths (unify)


@router.post("/album", status_code=status.HTTP_202_ACCEPTED)
async def add_album(album_info: AlbumInfoFromUser):
    await service.add_album(album_info)


@router.delete("/album/{album_id}")
async def delete_album(album_id: int):
    await AlbumDAO.delete(id=album_id)


# TODO: rework API: do not send all info at once, make endpoints for getting album's info
@router.get("/albums")
async def get_all_alumbs():
    albums = await AlbumDAO.get_all_with_tracks_and_artists()
    return albums


@router.post("/update_lyrics/{track_id}")
async def update_track_lyrics(track_id: int):
    await service.update_track_lyrics_by_id(track_id)


@router.post("/update_lyrics_karaoke/{track_id}")
async def update_track_lyrics_karaoke(track_id: int, data: LyricsKaraokeFromUser):
    await TrackDAO.update_lyrics_karaoke_by_id(track_id, data.lyrics_karaoke)
    return data


@router.post("/update_favorite/{track_id}")
async def update_track_favorite(track_id: int, data: IsFavoriteFromUser):
    await TrackDAO.update_favorite_by_id(track_id, data.is_favorite)
    return data


@router.post("/update_lyrics/")
async def update_all_tracks_lyrics():
    tracks = await TrackDAO.find_all()
    for i, track in enumerate(tracks):
        logger.info(f"Updating lyrics for track #{i}: {track.name}")
        try:
            await service.update_track_lyrics_by_id(track.id)
        except Exception:
            logger.error(f"Couldn't get lyrics for {track}, continuing..")
