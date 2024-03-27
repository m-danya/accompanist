<template>
  <div class="karaoke-lyrics">
    <AudioComponent
      :timeupdate="updateCurrentLine"
      :src="getStaticUrl(track.filename_instrumental)"
    />
    <div class="lyrics">
      <p class="current-line">{{ currentLineText }}</p>
      <p class="next-line">{{ nextLineText }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, inject, computed } from "vue";
import AudioComponent from "./AudioComponent.vue";

const props = defineProps({
  track: Object,
});

const currentLineIndex = ref(0);
const linesNumber = computed(() => props.track.lyrics_karaoke.length);
const currentLineText = computed(
  () => props.track.lyrics_karaoke[currentLineIndex.value].line
);
const nextLineText = computed(() => {
  if (currentLineIndex.value + 1 >= linesNumber.value) {
    return "";
  } else {
    return props.track.lyrics_karaoke[currentLineIndex.value + 1].line;
  }
});
const getStaticUrl = inject("getStaticUrl");

const updateCurrentLine = (currentTime) => {
  // sustainable for track rewinding

  let low = 0;
  let high = linesNumber.value - 1;
  let mid;
  if (currentTime < props.track.lyrics_karaoke[0].end_ts) {
    currentLineIndex.value = 0;
    return;
  }
  if (currentTime >= props.track.lyrics_karaoke[high].end_ts) {
    currentLineIndex.value = high;
    return;
  }
  while (low <= high) {
    mid = Math.floor((low + high) / 2);
    const midValEndTs = props.track.lyrics_karaoke[mid].end_ts;
    if (midValEndTs === currentTime) {
      currentLineIndex.value = mid;
      return;
    } else if (midValEndTs < currentTime) {
      low = mid + 1;
    } else {
      high = mid - 1;
    }
  }
  currentLineIndex.value = Math.max(0, low);
};
</script>

<style scoped>
.karaoke-lyrics .lyrics {
  white-space: pre-wrap;
  font-size: 20px;
  margin-top: 20px;
}

.current-line {
  font-weight: bold;
}

.next-line {
}
</style>
