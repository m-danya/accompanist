from functools import lru_cache
from pathlib import Path
from typing import List

import whisper


class LyricsTimestamper:
    MODEL_TYPE = "tiny"
    DEVICE = "cuda"

    def __init__(self) -> None:
        self.model = whisper.load_model(self.MODEL_TYPE).to(self.DEVICE)

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        @lru_cache(maxsize=None)
        def helper(i, j):
            if min(i, j) == 0:
                return max(i, j)
            elif s1[i - 1] == s2[j - 1]:
                return helper(i - 1, j - 1)
            else:
                return 1 + min(helper(i, j - 1), helper(i - 1, j), helper(i - 1, j - 1))

        return helper(len(s1), len(s2))

    def get_karaoke_lyrics(self, path_mp3: Path, lyrics: str) -> List[dict[str, str]]:
        # TODO: standardize lyrics preprocessing
        lyrics_lines = [
            line.strip()
            for line in lyrics.split("\n")
            if line.strip() and not line.startswith("[")
        ]

        transcript = self.model.transcribe(word_timestamps=True, audio=str(path_mp3))

        lyrics_karaoke = []
        segments = transcript["segments"]
        prev_n = 0
        for line in lyrics_lines:
            last_word = line[-1]
            curr_n = len(line)
            curr_segments = segments[prev_n:curr_n]

            min_lev_wordend = None
            min_lev_value = 1000000
            for segment in curr_segments:
                curr_word = segment["words"][0]["word"]
                curr_end = segment["words"][0]["end"]
                curr_lev_value = self._levenshtein_distance(curr_word, last_word)
                if min_lev_value > curr_lev_value:
                    min_lev_value = curr_lev_value
                    min_lev_wordend = curr_end

            prev_n = curr_n
            lyrics_karaoke.append({"line": line, "end_ts": min_lev_wordend})

        # TODO: assert that lines are sorted by "end_ts"
        print(lyrics_karaoke)
        return lyrics_karaoke
