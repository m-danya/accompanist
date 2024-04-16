from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from accompanist.collection.models import Album, Artist, Track
from accompanist.collection.schema import TrackUpdateRequest
from accompanist.dao import BaseDAO
from accompanist.database import async_session_maker
from accompanist.exceptions import AlbumNotFoundException, TrackNotFoundException


class ArtistDAO(BaseDAO):
    model = Artist


class AlbumDAO(BaseDAO):
    model = Album
    not_found_exception = AlbumNotFoundException

    @classmethod
    async def get_all(cls) -> list[dict]:
        async with async_session_maker() as session:
            query = (
                select(Album)
                .options(selectinload(Album.artist))
                .order_by(Album.added_at.desc())
            )
            result = await session.execute(query)
            albums = result.scalars().all()
        return [album.to_json() for album in albums]

    @classmethod
    async def get_by_id_with_tracks_info(cls, id_: int) -> list[dict]:
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=id_)
                .options(selectinload(Album.tracks), selectinload(Album.artist))
            )
            result = await session.execute(query)
            album = result.scalars().one_or_none()
        if not album:
            raise AlbumNotFoundException(id=id_)
        return album.to_json_with_tracks()


class TrackDAO(BaseDAO):
    model = Track
    not_found_exception = TrackNotFoundException

    @classmethod
    async def get_with_artist(cls, id_: int) -> Optional[Track]:
        async with async_session_maker() as session:
            query = select(Track).filter_by(id=id_).options(selectinload(Track.artist))
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def update(cls, track_id: int, update_request: TrackUpdateRequest):
        update_data = update_request.model_dump(exclude_unset=True)
        async with async_session_maker() as session:
            query = select(Track).filter_by(id=track_id).with_for_update()
            result = await session.execute(query)
            track = result.scalars().one_or_none()
            if not track:
                raise cls.not_found_exception(id=track_id)

            for field, value in update_data.items():
                setattr(track, field, value)

            await session.commit()
            return track.to_json()
