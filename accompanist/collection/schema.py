from pydantic import BaseModel


class AlbumInfoFromUser(BaseModel):
    search_query: str


class LyricsKaraokeFromUser(BaseModel):
    lyrics_karaoke: list[dict]


class IsFavoriteFromUser(BaseModel):
    is_favorite: bool
