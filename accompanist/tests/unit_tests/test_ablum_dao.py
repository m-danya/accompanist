import pytest

from accompanist.collection.dao import AlbumDAO
from accompanist.exceptions import AlbumNotFoundException


async def test_get_all_albums(test_album_data):
    albums = await AlbumDAO.get_all()
    assert len(albums) == len(test_album_data)

    for album in albums:
        test_album = next(
            test_album
            for test_album in test_album_data
            if test_album["id"] == album["id"]
        )

        assert album["id"] == test_album["id"]
        assert album["name"] == test_album["name"]
        assert album["cover_path"] == test_album["cover_path"]
        assert album["artist"]["id"] == test_album["artist_id"]


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
    except AlbumNotFoundException:
        if not must_exist:
            return
    if not must_exist:
        raise AssertionError("This album shouldn't exist")
    album_data = next(album for album in test_album_data if album["id"] == id_)
    for attr in ("id", "name", "cover_path"):
        assert album[attr] == album_data[attr]
    assert album["artist"]["id"] == album_data["artist_id"]
    assert len(album["tracks"]) == 2
