import whisper
import json
import yaml
from functools import lru_cache

from typing import List


class Timestamper:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path

        with open(self.data_path, "r") as config:
            model_cfg = yaml.safe_load(config)
            model_type = model_cfg["type"]
            device = model_cfg["device"]
        self.model = whisper.load_model(model_type).to(device)

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

    def get_line_timestamps(
        self, path_mp3: str, path_text: str
    ) -> List[dict[str, str]]:
        with open(path_text, "r") as f:
            text_lines = f.readlines()

        transcript = self.model.transcribe(word_timestamps=True, audio=path_mp3)

        output_data = []
        segments = transcript["segments"]
        prev_n = 0
        for line in text_lines:
            last_word = line[-1]
            curr_n = len(line)
            curr_segments = segments[prev_n:curr_n]

            min_lev_wordend = None
            min_lev_value = 1000000
            for segment in curr_segments:
                curr_word = segment["words"][0]["word"]
                curr_end = segments["words"][0]["end"]
                curr_lev_value = self._levenshtein_distance(curr_word, last_word)
                if min_lev_value > curr_lev_value:
                    min_lev_value = curr_lev_value
                    min_lev_wordend = curr_end

            prev_n = curr_n
            output_data.append({"line": line, "end_ts": min_lev_wordend})

        return output_data
