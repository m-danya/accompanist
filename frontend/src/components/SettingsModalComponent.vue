<template>
  <div class="modal-overlay" @click="$emit('closeModal')">
    <div class="modal-content" @click.stop>
      <button @click="$emit('closeModal')" class="close-button">
        <FontAwesomeIcon class="icon-sized" :icon="faXmark" fixed-width />
      </button>
      <div class="autoplay-checkbox">
        <input
          type="checkbox"
          id="autoplay"
          v-model="userSettings.isAutoplayEnabled"
          class="checkbox"
        />
        <label for="autoplay" class="label">Автовоспроизведение</label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, defineEmits } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faXmark } from "@fortawesome/free-solid-svg-icons";

const userSettings = inject("userSettings");

const emit = defineEmits(["closeModal"]);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure the modal is above other content */
}

.modal-content {
  position: relative;
  background-color: white;
  padding: 40px; /* Increased padding to give space for the close button */
  border-radius: 5px;
  max-width: 600px; /* Adjust based on your content needs */
  width: 90%; /* Responsive width */
  box-sizing: border-box;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333; /* Adjust color as needed */
}

.autoplay-checkbox {
  display: flex;
  align-items: center;
  font-family: Arial, sans-serif;
}

.checkbox {
  margin-right: 8px; /* Расстояние между чекбоксом и надписью */
}

.label {
  cursor: pointer; /* Указатель курсора изменяется при наведении на надпись */
  user-select: none; /* Отключает выделение текста надписи */
}
</style>
