from contextlib import redirect_stdout
from os import devnull

import lyricsgenius

from accompanist.config import settings


def get_lyrics_from_genius(artist_name: str, song_name: str):
    genius = lyricsgenius.Genius(settings.GENIUS_CLIENT_ACCESS_TOKEN)

    # Keep section headers (e.g. [Chorus]) in lyrics
    genius.remove_section_headers = False

    with open(devnull, "w") as fnull:
        # disable `print`s in this function
        with redirect_stdout(fnull):
            song = genius.search_song(
                title=song_name,
                artist=artist_name,
                get_full_info=False,
            )
    lyrics = song.lyrics

    # `lyricsgenius` parser makes some mistakes => fix them (maybe one day it
    #  will be fixed)
    first_newline = lyrics.find("\n")
    if lyrics[first_newline + 1] == "\n":
        from_idx = first_newline + 2
    else:
        from_idx = first_newline + 1
    lyrics = lyrics[from_idx:]
    if lyrics.endswith("Embed"):
        lyrics = lyrics[: -len("Embed")]
    lyrics = lyrics.replace("You might also like", "\n")

    # remove digits from "pyong" counter from the end of lyrics
    n_digits = 0
    while lyrics[-n_digits - 1].isdecimal():
        n_digits += 1

    if n_digits:
        lyrics = lyrics[:-n_digits]

    return lyrics
