from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from accompanist.database import Base


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    added_at: Mapped[date] = mapped_column(Date)

    def __str__(self):
        return f'Artist "{self.name}"'


class Album(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"))
    cover_path: Mapped[str]
    added_at: Mapped[date] = mapped_column(Date)

    artist: Mapped["Artist"] = relationship(back_populates="album")

    def __str__(self):
        return f'Album "{self.title}" by "{self.artist.name}"'
