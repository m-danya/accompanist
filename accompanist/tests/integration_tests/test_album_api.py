import pytest
from httpx import AsyncClient

# json for POST requests
# params for GET requests


# TODO: test `add_album` route, probably mocking the celery task execution


@pytest.mark.parametrize(
    "id_,status_code,error_detail",
    [
        (57, 200, None),
        (42, 404, "There is no album with {'id': 42}"),
    ],
)
async def test_get_album(id_, status_code, error_detail, ac: AsyncClient):
    response = await ac.get(f"/album/{id_}")
    assert response.status_code == status_code
    if not response.is_success:
        assert response.json()["detail"] == error_detail


@pytest.mark.parametrize(
    "id_,status_code,error_detail",
    [
        (57, 200, None),
        (42, 404, "There is no album with {'id': 42}"),
    ],
)
async def test_delete_album(id_, status_code, error_detail, ac: AsyncClient):
    response = await ac.delete(f"/album/{id_}")
    assert response.status_code == status_code
    if not response.is_success:
        assert response.json()["detail"] == error_detail


async def test_get_all_alumbs(ac: AsyncClient):
    response = await ac.get("/albums")
    assert response.status_code == 200
