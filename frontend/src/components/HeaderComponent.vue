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
      <FontAwesomeIcon class="icon-sized" :icon="faArrowsRotate" fixed-width />
    </div>
    <SettingsModalComponent v-if="isModalVisible" @closeModal="toggleModal" />
    <div class="settings-button" @click="toggleModal">
      <FontAwesomeIcon class="icon-sized" :icon="faGear" fixed-width />
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { defineEmits } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faArrowsRotate, faGear } from "@fortawesome/free-solid-svg-icons";
import SettingsModalComponent from "./SettingsModalComponent.vue";

const logo = ref(new URL("@/assets/logo.png", import.meta.url).href);
const emit = defineEmits(["refreshAlbums, handleGoToAlbumChoosing"]);

const isModalVisible = ref(false);

function toggleModal() {
  isModalVisible.value = !isModalVisible.value;
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  padding: 30px 0 0 50px;
  flex-wrap: wrap; /* Allows items to wrap to the next line on small screens */
  padding: 20px; /* Adjusted padding for responsiveness */
  gap: 20px; /* Adds space between flex items */
  justify-content: space-between; /* Spreads out the items on larger screens */
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
  /* margin-right: 50px; */

  cursor: pointer;
  display: flex;
  align-items: center;
}

.settings-button {
  /* margin-left: auto; */
  /* margin-right: 50px; */
  cursor: pointer;
  display: flex;
  align-items: center;
}

.icon-sized {
  width: 24px;
  /* Adjust icon size as needed */
  height: 24px;
  /* Adjust icon size as needed */
}
</style>
