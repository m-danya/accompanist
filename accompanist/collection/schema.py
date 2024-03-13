from pydantic import BaseModel


class AlbumInfoFromUser(BaseModel):
    search_query: str
