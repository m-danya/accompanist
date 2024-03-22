<template>
  <div>
    <!--TODO: use AudioComponent here?-->
    <audio ref="audioPlayer" :src="mp3Url" @loadedmetadata="setupPlayer" controls></audio>
    <button @click="recordTimecode">Следующая строка</button>
    {{ lyricsLines[currentLineIndex] }}
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
    audioPlayer.value.play();
    startTime = audioPlayer.value.currentTime;
  }
};

const recordTimecode = () => {
  const endTime = audioPlayer.value.currentTime;
  lyricsWithTimecodes.push({
    line: lyricsLines[currentLineIndex.value],
    end_ts: endTime - startTime,
  });
  if (currentLineIndex.value == lyricsLines.length - 1) {
    console.log(lyricsWithTimecodes);
    emit("sendRecordedKaraokeLyrics", lyricsWithTimecodes);
    return;
  }
  currentLineIndex.value++;
};
</script>
