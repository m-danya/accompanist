<template>
  <div class="container">
    <div class="album-list">
      <h1>Доступные альбомы</h1>
      <div class="albums-grid">
        <div class="album" v-for="album in albums" :key="album.id" @click="emitSelect(album)">
          <img :src="getImageUrl(album.cover_path)" alt="Обложка альбома" class="album-cover">
          <div class="album-title">{{ album.name }}</div>
          <div class="album-artist">{{ album.artist.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject, defineEmits } from 'vue';

const backendAddress = inject('backendAddress')
const albums = inject('albums')

const emit = defineEmits(['selectAlbum']);

function emitSelect(album) {
  emit('selectAlbum', album);
}

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
</style>