import json
from pathlib import Path
from typing import List

import librosa
import torch
from transformers import (
    WhisperForConditionalGeneration,
    WhisperTokenizer,
    WhisperProcessor,
)
from accompanist.config import settings
from openai import OpenAI


class LyricsTimestamper:
    MODEL_TYPE = "small"

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperForConditionalGeneration.from_pretrained(
            "openai/whisper-small",
        ).to(self.device)
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        self.tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-small")
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_karaoke_lyrics(self, vocals_mp3: Path, lyrics: str) -> List[dict[str, str]]:
        # TODO: refactor this long method
        # TODO: move calling this method to celery task
        # TODO: standardize lyrics preprocessing between frontend and backend
        lyrics_lines = [
            line.strip()
            for line in lyrics.split("\n")
            if line.strip() and not line.startswith("[")
        ]

        sampling_rate = 16_000  # as Whisper requires?
        waveform, _ = librosa.load(vocals_mp3, sr=sampling_rate, mono=True)

        chunk_length_s = 5
        overlap = chunk_length_s / 2  # 50% overlap
        chunk_samples = int(chunk_length_s * sampling_rate)
        overlap_samples = int(overlap * sampling_rate)

        chunks = [
            waveform[i : i + chunk_samples]
            for i in range(
                0, len(waveform) - chunk_samples, chunk_samples - overlap_samples
            )
        ]

        transcribed_lines = []
        for i, chunk in enumerate(chunks):
            start_sample = i * (chunk_samples - overlap_samples)
            end_sample = start_sample + len(chunk)

            inputs = self.processor(
                chunk, return_tensors="pt", sampling_rate=sampling_rate
            ).input_features
            inputs = inputs.to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(inputs, language="ru")

            transcribed_text = self.processor.decode(
                outputs[0], skip_special_tokens=True
            )

            start_ts = start_sample / sampling_rate
            end_ts = end_sample / sampling_rate

            transcribed_lines.append(
                {"text": transcribed_text, "start_ts": start_ts, "end_ts": end_ts}
            )

        system_prompt = """
        You're a deaf person at a local karaoke bar. Your job is to make
        timestamps for karaoke songs. For each song you get `lyrics_lines` an
        array of ground truth lines and`transcribed_lines`, which is an array of
        speech-to-text model. You need to output a `lyrics_karaoke` list, each
        object of which is a dict with keys "line" and "end_ts". In other words,
        you need to find an end of every line in the text. 

        `lyrics_karaoke` array must have exactly the same lines as `lyrics_lines` in
        exactly the same order. Values of `end_ts` must increase from one element to
        another, as they are lines of one song.

        Do not write any code, just output the `lyrics_karaoke` dict in a JSON format.
        Try your best.
        """
        user_request = f"{lyrics_lines=}\n\n{transcribed_lines=}"
        print(user_request)
        completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_request,
                },
            ],
        )
        lyrics_karaoke = completion.choices[0].message.content
        lyrics_karaoke = json.loads(
            lyrics_karaoke.strip().replace("```json", "").replace("```", "")
        )
        try:
            lyrics_karaoke = lyrics_karaoke["lyrics_karaoke"]
        except Exception:
            pass
        print(lyrics_karaoke)
        return lyrics_karaoke
