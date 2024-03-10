from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accompanist.database import Base


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    albums: Mapped[list["Album"]] = relationship(back_populates="artist")
    songs: Mapped[list["Song"]] = relationship(back_populates="artist")

    def __str__(self):
        return f'Artist "{self.name}"'


class Song(Base):
    __tablename__ = "song"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"))
    album_id: Mapped[int] = mapped_column(ForeignKey("album.id"))
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    album: Mapped["Album"] = relationship(back_populates="songs")
    artist: Mapped["Artist"] = relationship(back_populates="songs")

    def __str__(self):
        return f'Song "{self.name}" by "{self.artist.name}"'


class Album(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"))
    cover_path: Mapped[str]
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    source_url: Mapped[str]

    artist: Mapped["Artist"] = relationship(back_populates="albums")
    songs: Mapped[list["Song"]] = relationship(back_populates="album")

    def __str__(self):
        return f'Album "{self.name}" by "{self.artist.name}"'
