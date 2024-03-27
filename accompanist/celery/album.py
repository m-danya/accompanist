import asyncio
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from uuid import uuid4

from loguru import logger
from ytmusicapi import YTMusic

from accompanist.collection.dao import AlbumDAO, ArtistDAO, TrackDAO
from accompanist.collection.service_genius import get_lyrics_from_genius
from accompanist.config import settings


# TODO: manage/clean files that are not referenced in the database?
def get_path_in_storage(extension: str):
    return settings.STORAGE_PATH / f"{uuid4().hex}.{extension}"


# Note: this function may be unreliable, but it works, as opposed to simple
# `asyncio.run` call, idk why (where does the other event loop comes from in a
# fully sync celery worker process?)
def run_async(coroutine):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Existing event loop is closed.")
    except RuntimeError:
        # If no event loop is available or it is closed, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)


def process_album(search_query: str):
    ytmusic = YTMusic(language=settings.YOUTUBE_LANGUAGE)
    search_results = ytmusic.search(search_query, filter="albums")
    album_id = search_results[0]["browseId"]
    album_json = ytmusic.get_album(album_id)

    # TODO: somehow get better album cover's resolution than 512x512, e.g. from
    #  Genius.com API / python wrapper for this API
    best_thumbnail_url = album_json["thumbnails"][-1]["url"]
    cover_path = get_path_in_storage("jpg")
    urllib.request.urlretrieve(best_thumbnail_url, cover_path)

    # TODO: think about feat albums and incorrect order if that occurs
    artist_name = album_json["artists"][0]["name"]

    coroutine = ArtistDAO.find_one_or_none(name=artist_name)
    artist = run_async(coroutine)

    if artist is None:
        coroutine = ArtistDAO.add(name=artist_name)
        artist = run_async(coroutine)
    logger.info(f"Artist {artist}")

    coroutine = AlbumDAO.add(
        name=album_json["title"],
        artist_id=artist.id,
        cover_path=str(cover_path.relative_to(settings.STORAGE_PATH)),
        source_info=album_json,
    )
    album = run_async(coroutine)
    logger.info(f"Added {album}")

    for i, track in enumerate(album_json["tracks"], start=1):
        vocals_path, instrumental_path, original_path = process_track(track["videoId"])
        track_name = track["title"]
        lyrics = None
        try:
            lyrics = get_lyrics_from_genius(artist.name, track_name)
        except Exception:
            logger.exception(f"Couldn't get lyrics for {track_name}, continuing..")
        coroutine = TrackDAO.add(
            name=track_name,
            artist_id=artist.id,
            album_id=album.id,
            filename_vocals=str(vocals_path.relative_to(settings.STORAGE_PATH)),
            filename_instrumental=str(
                instrumental_path.relative_to(settings.STORAGE_PATH)
            ),
            filename_original=str(original_path.relative_to(settings.STORAGE_PATH)),
            number_in_album=i,
            duration=track["duration"],
            lyrics=lyrics,
        )
        track = run_async(coroutine)
        logger.info(f"Added {track}")


def process_track(video_id: str) -> tuple[Path, Path, Path]:
    with tempfile.TemporaryDirectory() as tempdir_yt, tempfile.TemporaryDirectory() as tempdir_demucs:
        output_dir_yt = Path(tempdir_yt)
        output_dir_demucs = Path(tempdir_demucs)

        # 1. Download yt video and extract audio from it
        subprocess.run(
            [
                "yt-dlp",
                "--rm-cache-dir",
                "--extract-audio",
                "--audio-format",
                "mp3",
                "--no-playlist",
                "-o",
                f"{output_dir_yt}/%(title)s.%(ext)s",
                "--",
                str(video_id),
            ]
        )

        original_tmp_path = next(output_dir_yt.iterdir())
        logger.info("Running demucs..")
        # 2. Run demucs and leave instrumental only
        subprocess.run(
            [
                "demucs",
                "--mp3",
                "--two-stems=vocals",
                str(original_tmp_path),
                "-o",
                str(output_dir_demucs),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # 3. Move files to the storage from the temporary directory

        vocals_path = get_path_in_storage("mp3")
        instrumental_path = get_path_in_storage("mp3")
        original_path = get_path_in_storage("mp3")

        # (mp3 files are nested deep inside the output dir => call recursive glob)
        shutil.move(next(output_dir_demucs.rglob("vocals.mp3")), vocals_path)
        shutil.move(next(output_dir_demucs.rglob("no_vocals.mp3")), instrumental_path)
        shutil.move(original_tmp_path, original_path)

    return vocals_path, instrumental_path, original_path
