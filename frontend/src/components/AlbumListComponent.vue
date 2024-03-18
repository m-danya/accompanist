<template>
  <div class="container">
    <div class="album-list">
      <h2>Доступные альбомы</h2>
      <div class="albums-grid">
        <div
          class="album"
          v-for="album in props.albums"
          :key="album.id"
          @click="$emit('selectAlbum', album.id)"
        >
          <img
            :src="getImageUrl(album.cover_path)"
            alt="Обложка альбома"
            class="album-cover clickable"
          />
          <div class="album-title clickable">{{ album.name }}</div>
          <div class="album-artist clickable">{{ album.artist.name }}</div>
        </div>
        <div class="album-cover new-album" @click="$emit('uploadNewAlbum')">
          <span class="plus-sign">+</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, defineEmits, defineProps } from "vue";

const backendAddress = inject("backendAddress");

const props = defineProps({
  albums: Array[Object],
});

const emit = defineEmits(["selectAlbum", "uploadNewAlbum"]);

const getImageUrl = (image_name) => {
  return `${backendAddress}/static/${image_name}`;
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  /* Максимальная ширина контейнера */
  margin: 0 auto;
  /* Центрирование контейнера */
  padding: 20px;
  /* Отступы внутри контейнера */
}

.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  justify-items: center;
  /* Центрирует содержимое ячеек по горизонтали */
}

.album {
  display: flex;
  flex-direction: column;
  align-items: start;
  /* Aligns items to the start of the container (left) */
}

.album-cover {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
  /* Adds space between the image and the text */
}

.album-title {
  font-size: 16px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 5px;
}

.album-artist {
  font-size: 14px;
  text-align: left;
  /* Aligns text to the left */
}

.new-album {
  border: 2px dashed #ccc;
  /* Dashed border for the new album square */
  display: flex;
  /* Use flexbox for centering */
  justify-content: center;
  /* Center children horizontally */
  align-items: center;
  /* Center children vertically */
  cursor: pointer;
}

.plus-sign {
  color: #888;
  /* Color of the plus sign */
  font-size: 48px;
  /* Adjust this value to make the plus sign larger */
  font-weight: bold;
  display: flex;
  /* Ensures the text itself is flex, helping with centering */
  justify-content: center;
  /* Center content horizontally */
  align-items: center;
  /* Center content vertically */
}

h2 {
  padding-bottom: 40px;
}
</style>
