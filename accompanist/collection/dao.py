from typing import Optional

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
    async def get_all_with_tracks_and_artists(cls) -> list[dict]:
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

    @classmethod
    async def get_for_update_with_artist(cls, id: int) -> Optional[Track]:
        async with async_session_maker() as session:
            query = (
                select(Track)
                .filter_by(id=id)
                .options(selectinload(Track.artist))
                .with_for_update()
            )
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def update_lyrics(cls, track: Track, lyrics: str):
        async with async_session_maker() as session:
            track.lyrics = lyrics
            session.add(track)
            await session.commit()
