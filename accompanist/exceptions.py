from fastapi import HTTPException, status


class AccompanistException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(
            status_code=self.status_code,
            detail=self._detail if hasattr(self, "_detail") else self.detail,
        )


class EntityNotFoundException(AccompanistException):
    status_code = status.HTTP_404_NOT_FOUND
    entity_name = "entity"

    def __init__(self, **filter_criteria):
        self.filter_criteria = filter_criteria
        super().__init__()

    @property
    def _detail(self):
        return f"There is no {self.entity_name} with {self.filter_criteria}"


class AlbumNotFoundException(EntityNotFoundException):
    entity_name = "album"


class TrackNotFoundException(EntityNotFoundException):
    entity_name = "track"
