<template>
  <div id="app">
    <AddAlbumComponent />
    <AlbumComponent :album="selectedAlbum" v-if="selectedAlbum" />
    <AlbumListComponent @selectAlbum="handleSelectAlbum" />
  </div>
</template>


<script setup>
import AddAlbumComponent from './components/AddAlbumComponent.vue';
import AlbumComponent from './components/AlbumComponent.vue';
import AlbumListComponent from './components/AlbumListComponent.vue';


import { onMounted, provide, ref } from 'vue';


const _backendHost = process.env.VUE_APP_BACKEND_HOST || 'localhost';
const _backendPort = process.env.VUE_APP_BACKEND_PORT || 8000;
const backendAddress = `http://${_backendHost}:${_backendPort}`
provide('backendAddress', backendAddress)

const albums = ref([]);
const selectedAlbum = ref(null); // album object
provide('albums', albums)

function handleSelectAlbum(album_id) {
  selectedAlbum.value = album_id
}

const fetchAlbums = async () => {
  try {
    const response = await fetch(`${backendAddress}/collection/albums`);
    if (!response.ok) throw new Error('Failed to fetch');
    albums.value = await response.json();
  } catch (error) {
    console.error('Error fetching albums:', error);
  }
};

onMounted(() => {
  fetchAlbums();
});


</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
  background-color: #fafafa;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: 'Roboto', sans-serif;

}
</style>