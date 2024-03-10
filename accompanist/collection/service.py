from accompanist.collection.dao import ArtistDAO, AlbumDAO
from accompanist.collection.schema import AlbumInfoFromUser


async def add_album(album_info: AlbumInfoFromUser):
    artist_name = album_info.artist_name
    artist = await ArtistDAO.find_one_or_none(name=artist_name)
    if artist is None:
        artist = await ArtistDAO.add(name=artist_name)
    album = await AlbumDAO.add(
        name=album_info.name,
        artist_id=artist.id,
        cover_path="https://placehold.jp/3d4070/ffffff/150x150.png",
        source_url=album_info.url,
    )
    return album
