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
import { ref, defineProps, onMounted, inject } from "vue";
import AudioComponent from "./AudioComponent.vue";

const props = defineProps({
  track: Object,
});

const currentLineIndex = ref(0);
const currentLineText = ref("");
const nextLineText = ref("");
const getStaticUrl = inject("getStaticUrl");

// TODO: rewrite these two functions

const updateCurrentLine = (currentTime) => {
  let foundIndex = null;
  props.track.lyrics_karaoke.forEach((item, index) => {
    if (currentTime <= item.end_ts) {
      if (foundIndex === null) {
        foundIndex = index;
      }
    }
  });

  if (foundIndex !== null && foundIndex !== currentLineIndex.value) {
    currentLineIndex.value = foundIndex;
    currentLineText.value = props.track.lyrics_karaoke[foundIndex].line;
    const nextLine = props.track.lyrics_karaoke[foundIndex + 1];
    nextLineText.value = nextLine ? nextLine.line : "";
  }
};

onMounted(() => {
  if (props.track.lyrics_karaoke && props.track.lyrics_karaoke.length) {
    currentLineText.value = props.track.lyrics_karaoke[0].line;
    nextLineText.value =
      props.track.lyrics_karaoke.length > 1
        ? props.track.lyrics_karaoke[1].line
        : "";
  }
});
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
