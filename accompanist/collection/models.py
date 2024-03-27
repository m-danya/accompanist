from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accompanist.database import Base

# TODO: add unique constraints for songs and albums


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    albums: Mapped[list["Album"]] = relationship(back_populates="artist")
    tracks: Mapped[list["Track"]] = relationship(back_populates="artist")

    def __repr__(self):
        return f'Artist "{self.name}"'

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Track(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"))
    album_id: Mapped[int] = mapped_column(ForeignKey("album.id", ondelete="CASCADE"))
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    filename_vocals: Mapped[str]
    filename_instrumental: Mapped[str]
    filename_original: Mapped[str]
    number_in_album: Mapped[int]
    duration: Mapped[str]
    lyrics: Mapped[Optional[str]]
    lyrics_karaoke: Mapped[Optional[list[dict]]] = mapped_column(JSON)
    is_favorite: Mapped[bool] = mapped_column(default=False)

    album: Mapped["Album"] = relationship(back_populates="tracks")
    artist: Mapped["Artist"] = relationship(back_populates="tracks")

    def __repr__(self):
        return f'track "{self.name}" by "{self.artist.name}"'

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "filename_vocals": self.filename_vocals,
            "filename_instrumental": self.filename_instrumental,
            "filename_original": self.filename_original,
            "number_in_album": self.number_in_album,
            "duration": self.duration,
            "lyrics": self.lyrics,
            "lyrics_karaoke": self.lyrics_karaoke,
            "is_favorite": self.is_favorite,
        }


class Album(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"))
    cover_path: Mapped[str]
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    source_info: Mapped[dict] = mapped_column(JSON)

    artist: Mapped["Artist"] = relationship(back_populates="albums")
    tracks: Mapped[list["Track"]] = relationship(back_populates="album")

    def __repr__(self):
        return f'Album "{self.name}" by "{self.artist.name}"'

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "artist": self.artist.to_json(),
            "cover_path": self.cover_path,
            "tracks": sorted(
                (track.to_json() for track in self.tracks),
                key=lambda track: track["number_in_album"],
            ),
        }
