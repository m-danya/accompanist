import pytest

from accompanist.collection.dao import AlbumDAO
from accompanist.exceptions import NoAlbumException


async def test_get_all_albums():
    albums = await AlbumDAO.get_all()
    assert len(albums) == 1


@pytest.mark.parametrize(
    "id_,must_exist",
    [
        (57, True),
        (42, False),
    ],
)
async def test_get_by_id_with_tracks_info(id_, must_exist, test_album_data):
    try:
        album = await AlbumDAO.get_by_id_with_tracks_info(id_)
    except NoAlbumException:
        if not must_exist:
            return
    if not must_exist:
        raise AssertionError("This album shouldn't exist")
    album_data = next(album for album in test_album_data if album["id"] == id_)
    for attr in ("id", "name", "cover_path"):
        assert album[attr] == album_data[attr]
    assert album["artist"]["id"] == album_data["artist_id"]
    assert len(album["tracks"]) == 2


# TODO: add more tests for different DAOs
