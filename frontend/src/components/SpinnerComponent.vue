<template>
  <div class="spinner" :style="dynamicStyle"></div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from "vue";

const props = defineProps({
  size: String,
});

const dynamicStyle = computed(() => {
  return {
    "--dynamic-size": props.size,
  };
});
</script>

<style scoped>
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: var(--dynamic-size);
  height: var(--dynamic-size);
  -webkit-animation: spin 2s linear infinite;
  /* Safari */
  animation: spin 2s linear infinite;
  margin: auto;
}
</style>
