from pathlib import Path

import pytest

from accompanist.collection.timestamper import LyricsTimestamper


@pytest.mark.skip(reason="It requires an OpenAI API key")
def test_timestamper(test_track_data):
    timestamper = LyricsTimestamper()
    vocals_mp3_path = Path("accompanist/tests/melancholy_vocals.mp3")
    melancholy_track = next(
        track for track in test_track_data if track["name"] == "Меланхолия драйв"
    )
    lyrics_karaoke = timestamper.get_karaoke_lyrics(
        vocals_mp3_path, melancholy_track["lyrics"]
    )
    assert lyrics_karaoke
    # TODO: move preprocessing to model's property or somewhere else
    lyrics_lines_preprocessed = [
        line.strip()
        for line in melancholy_track["lyrics"].split("\n")
        if line.strip() and not line.startswith("[")
    ]
    for original_line, karaoke_line in zip(lyrics_lines_preprocessed, lyrics_karaoke):
        assert original_line == karaoke_line["line"]
    # TODO: assert non-descending of `end_ts` sequence
