from copy import deepcopy

import pytest

from accompanist.collection.dao import TrackDAO
from accompanist.collection.schema import TrackUpdateRequest
from accompanist.exceptions import TrackNotFoundException


@pytest.mark.parametrize(
    "id_,must_exist",
    [
        (698, True),
        (42, False),
    ],
)
async def test_get_with_artist(id_, must_exist, test_track_data):
    track = await TrackDAO.get_with_artist(id_)
    if not must_exist:
        assert not track
        return
    test_track = next(track for track in test_track_data if track["id"] == id_)
    assert track.id == test_track["id"]


@pytest.mark.parametrize(
    "id_,must_exist,update_request",
    [
        (698, True, TrackUpdateRequest(is_favorite=False)),
        (698, True, TrackUpdateRequest(is_favorite=True)),
        (698, True, TrackUpdateRequest(lyrics="Na na na", is_favorite=True)),
        (698, True, TrackUpdateRequest(lyrics="Na na na", is_favorite=False)),
        (698, True, TrackUpdateRequest(lyrics="Na na na", genius_url="genius.com/123")),
        (42, False, TrackUpdateRequest(lyrics="Na na na")),
    ],
)
async def test_update_track(id_, must_exist, update_request, test_track_data):
    if must_exist:
        track_original_json = (await TrackDAO.get_with_artist(id_)).to_json()
    try:
        returned_track_json = await TrackDAO.update(id_, update_request)
        updated_track_json = (await TrackDAO.get_with_artist(id_)).to_json()
    except TrackNotFoundException:
        if not must_exist:
            return
    if not must_exist:
        raise AssertionError("This track must not exist")
    assert updated_track_json == returned_track_json

    updated_track_ground_truth = deepcopy(track_original_json)
    updated_track_ground_truth.update(update_request.model_dump(exclude_unset=True))

    assert updated_track_json == updated_track_ground_truth
