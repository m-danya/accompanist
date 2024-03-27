<template>
  <div class="karaoke-player">
    <!--TODO: use AudioComponent here?-->
    <audio
      ref="audioPlayer"
      :src="mp3Url"
      @loadedmetadata="setupPlayer"
      controls
      class="audio-player"
    ></audio>
    <div class="controls">
      <button @click="recordTimecode" class="btn next-line">
        Следующая строка
      </button>
      <button @click="recordInterludeEnd" class="btn end-interlude">
        Конец проигрыша
      </button>
    </div>
    <div class="lyrics">{{ lyricsLines[currentLineIndex] }}</div>
  </div>
</template>

<script setup>
import { ref, reactive, defineProps, defineEmits } from "vue";

const props = defineProps({
  mp3Url: String,
  lyricsText: String,
});
const emit = defineEmits(["sendRecordedKaraokeLyrics"]);

const audioPlayer = ref(null);
const lyricsLines = props.lyricsText
  .split("\n")
  .filter((line) => line.trim() && !line.trim().startsWith("["));
const lyricsWithTimecodes = reactive([]);
let currentLineIndex = ref(0);
let startTime = 0;

const setupPlayer = () => {
  if (audioPlayer.value) {
    audioPlayer.value.addEventListener("play", () => {
      startTime = audioPlayer.value.currentTime;
    });
    audioPlayer.value.play();
  }
};

const recordTimecode = () => {
  const endTime = audioPlayer.value.currentTime;
  lyricsWithTimecodes.push({
    line: lyricsLines[currentLineIndex.value],
    end_ts: endTime - startTime,
  });
  if (currentLineIndex.value == lyricsLines.length - 1) {
    emit("sendRecordedKaraokeLyrics", lyricsWithTimecodes);
    return;
  }
  currentLineIndex.value++;
};

const recordInterludeEnd = () => {
  const endTime = audioPlayer.value.currentTime;
  lyricsWithTimecodes.push({
    line: "[Проигрыш]",
    end_ts: endTime - startTime,
  });
};
</script>

<style scoped>
.karaoke-player {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  font-family: "Arial", sans-serif;
}

.audio-player {
  max-width: 600px;
  width: 100%;
}

.controls {
  display: flex;
  gap: 10px;
}

.btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.btn:hover {
  background-color: #1f77be;
}

.btn:active {
  background-color: #2196f3;
}

.lyrics {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
  text-align: center;
}
</style>
