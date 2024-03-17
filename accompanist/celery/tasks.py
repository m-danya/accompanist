from loguru import logger

from accompanist.celery.album import process_album
from accompanist.celery.main import app

# TODO: ensure only one GPU-requiring task is running at each moment of time


@app.task(
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=False,
)
def process_album_task(search_query: str):
    # TODO: make this task idemponent by using/ignoring the same albums/songs if they
    # already exist (because of previously run task, which failed at some point)
    try:
        process_album(search_query)
    except Exception:
        logger.exception("Celery task `process_album_task` has failed")
        raise
