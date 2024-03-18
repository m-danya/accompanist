<template>
  <header class="header">
    <img
      :src="logo"
      alt="Accompanist Logo"
      class="logo clickable"
      @click="$emit('goToAlbumChoosing')"
    />
    <h1 class="clickable" @click="$emit('goToAlbumChoosing')">Accompanist</h1>
    <div class="refresh-button" @click="$emit('refreshAlbums')">
      <svg
        class="icon-refresh"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M23 4v6h-6"></path>
        <path d="M1 20v-6h6"></path>
        <path d="M3.51 9a9 9 0 0 1 14.98-3L21 10"></path>
        <path d="M20.49 15a9 9 0 0 1-14.98 3L3 14"></path>
      </svg>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { defineEmits } from "vue";

const logo = ref(new URL("@/assets/logo.png", import.meta.url).href);
const emit = defineEmits(["refreshAlbums, handleGoToAlbumChoosing"]);
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  padding: 30px 0 0 50px;
}

.logo {
  width: 50px;
  height: auto;
  margin-right: 10px;
}

h1 {
  margin: 0;
  font-size: 24px;
}

.refresh-button {
  margin-left: auto;
  margin-right: 50px;
  /* Moves the button to the far right */
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
}

.icon-refresh {
  width: 24px;
  /* Adjust icon size as needed */
  height: 24px;
  /* Adjust icon size as needed */
}
</style>
