from pydantic import BaseModel


class AlbumInfoFromUser(BaseModel):
    name: str
    artist_name: str
    url: str
