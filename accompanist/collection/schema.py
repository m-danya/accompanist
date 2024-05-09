from typing import Optional

from pydantic import BaseModel


class AlbumInfoFromUser(BaseModel):
    search_query: str


class TrackUpdateRequest(BaseModel):
    is_favorite: Optional[bool] = None
    lyrics: Optional[str] = None
    lyrics_karaoke: Optional[list[dict]] = None
    genius_url: Optional[str] = None
    notes: Optional[str] = None
