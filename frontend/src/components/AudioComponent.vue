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
          if (props.autocontinue) {
            // TODO: replace with something better (like `onFinish`)
            if (audioRef.duration - audioRef.currentTime < 0.5) {
              $emit('finishAudio');
            }
          }
        }
      }
    "
  ></audio>
</template>

<script setup>
import { defineProps, ref, defineEmits } from "vue";
const props = defineProps({
  src: String,
  autoplay: Boolean,
  autocontinue: Boolean,
  timeupdate: { type: Function, required: false, default: () => {} },
});
const emit = defineEmits(["finishAudio"]);

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
