from pathlib import Path

from accompanist.collection.recognizer import LyricsTimestamper


def test_timestamper(test_track_data):
    timestamper = LyricsTimestamper()
    vocals_mp3_path = Path("accompanist/tests/melancholy_vocals.mp3")
    melancholy_track = next(
        track for track in test_track_data if track["name"] == "Меланхолия драйв"
    )
    lyrics_karaoke = timestamper.get_karaoke_lyrics(
        vocals_mp3_path, melancholy_track["lyrics"]
    )
    # TODO: write asserts
