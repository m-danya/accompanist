from accompanist.collection.models import Album, Artist
from accompanist.dao import BaseDAO


class ArtistDAO(BaseDAO):
    model = Artist


class AlbumDAO(BaseDAO):
    model = Album
