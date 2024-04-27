from pathlib import Path
from typing import List

import librosa
import torch
from transformers import (
    WhisperForConditionalGeneration,
    WhisperTokenizer,
    WhisperProcessor,
)


class LyricsTimestamper:
    MODEL_TYPE = "small"

    def __init__(self) -> None:
        # self.pipe = pipeline(
        #     "automatic-speech-recognition",
        #     model="openai/whisper-small",
        #     chunk_length_s=30,
        #     device_map="auto",
        # )
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperForConditionalGeneration.from_pretrained(
            "openai/whisper-small",
        ).to(self.device)
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-small")
        self.tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-small")

    def get_karaoke_lyrics(self, vocals_mp3: Path, lyrics: str) -> List[dict[str, str]]:
        # TODO: standardize lyrics preprocessing between frontend and backend
        lyrics_lines = [
            line.strip()
            for line in lyrics.split("\n")
            if line.strip() and not line.startswith("[")
        ]

        # audio = whisper.load_audio(path_mp3)
        # audio = whisper.pad_or_trim(audio)

        # mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # _, probs = self.model.detect_language(mel)
        # options = whisper.DecodingOptions(language='ru')
        sampling_rate = 16_000  # as Whisper requires?
        waveform, _ = librosa.load(vocals_mp3, sr=sampling_rate, mono=True)

        # non_silent_intervals = librosa.effects.split(waveform, top_db=30)

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

        # transcribed_lines = []
        # for start_sample, end_sample in non_silent_intervals:
        #     interval_audio = waveform[start_sample:end_sample]

        # prediction = self.pipe(
        #     audio_dict,
        #     # as the pipeline does not support `language` kwarg and fails if
        #     #  autodetection finds two different languages in one batch
        #     batch_size=1,
        #     return_timestamps=True,
        # )["chunks"]

        print(f"{lyrics_lines=}")
        print(f"{transcribed_lines=}")
        prompt = """
        You're a deaf person at a local karaoke bar. Your job is to make timestamps
        for karaoke songs. For each song you get `lyrics_lines` an array of ground
        truth lines and`transcribed_lines`, which is an array of speech-to-text
        model. You need to output a `lyrics_karaoke` list, each object of which is a
        dict with keys "line" and "end_ts". In other words, you need to find an end
        of every line in the text. 

        `lyrics_karaoke` array must have exactly the same lines as `lyrics_lines` in
        exactly the same order. Values of `end_ts` must increase from one element to
        another, as they are lines of one song.

        Do not write any code, just output the `lyrics_karaoke` dict in a JSON format.
        Try your best. Here is your input:
        """
        lyrics_karaoke = "ChatGPT4(lyrics_lines, transcribed_lines, prompt)"
        return lyrics_karaoke
