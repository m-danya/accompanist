import pytest
from httpx import AsyncClient

# TODO: test `update_track_lyrics`, use `skipif` to detect whether Genius token
#  is specified or not in `.env` (e.g. in GH actions it won't be there)


@pytest.mark.parametrize(
    "id_,status_code,error_detail",
    [
        (702, 200, None),
        (42, 404, "There is no track with {'id': 42}"),
    ],
)
async def test_get_track(id_, status_code, error_detail, ac: AsyncClient):
    response = await ac.get(f"/track/{id_}")
    assert response.status_code == status_code
    if not response.is_success:
        assert response.json()["detail"] == error_detail
