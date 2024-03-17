import asyncio

from accompanist.celery.tasks import process_album_task
from accompanist.collection.dao import TrackDAO
from accompanist.collection.schema import AlbumInfoFromUser
from accompanist.collection.service_genius import get_lyrics_from_genius


async def add_album(album_info: AlbumInfoFromUser):
    process_album_task.delay(album_info.search_query)


async def update_track_lyrics_by_id(track_id: int):
    track = await TrackDAO.get_for_update_with_artist(track_id)
    loop = asyncio.get_running_loop()
    lyrics = await loop.run_in_executor(
        None, get_lyrics_from_genius, track.artist.name, track.name
    )
    await TrackDAO.update_lyrics(track, lyrics)
