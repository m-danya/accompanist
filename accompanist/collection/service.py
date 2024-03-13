from accompanist.collection.schema import AlbumInfoFromUser
from accompanist.celery.tasks import process_album_task


async def add_album(album_info: AlbumInfoFromUser):
    process_album_task.delay(album_info.search_query)
