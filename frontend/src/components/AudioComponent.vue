<template>
  <audio
    controls
    :src="props.src"
    type="audio/mpeg"
    ref="audioRef"
    @loadedmetadata="setupPlayer"
    @timeupdate="
      () => {
        if (audioRef) {
          props.timeupdate(audioRef.currentTime);
        }
      }
    "
  ></audio>
</template>

<script setup>
import { defineProps, ref } from "vue";
const props = defineProps({
  src: String,
  autoplay: Boolean,
  timeupdate: { type: Function, required: false, default: () => {} },
});

const audioRef = ref(null);

function setupPlayer() {
  if (props.autoplay && audioRef.value) {
    audioRef.value.play();
  }
}
</script>
<style scoped>
audio {
  width: 100%;
  margin-top: 10px;
}
</style>
