from sqlalchemy import select
from sqlalchemy.orm import selectinload

from accompanist.collection.models import Album, Artist, Track
from accompanist.dao import BaseDAO
from accompanist.database import async_session_maker


class ArtistDAO(BaseDAO):
    model = Artist


class AlbumDAO(BaseDAO):
    model = Album

    @classmethod
    async def get_all_with_tracks_and_artists(cls):
        async with async_session_maker() as session:
            query = select(cls.model).options(
                selectinload(Album.tracks), selectinload(Album.artist)
            )
            result = await session.execute(query)
            # TODO: think about using `mappings()`
            albums = result.scalars().all()
        return [album.to_json() for album in albums]


class TrackDAO(BaseDAO):
    model = Track
