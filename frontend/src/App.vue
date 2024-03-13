<template>
  <div id="app">
    <HeaderComponent @click="handleGoToAlbumChoosing" />
    <AddAlbumComponent v-if="appState === AppStates.UploadingNewAlbum"
      @confirmUploadNewAlbum="handleConfirmUploadNewAlbum" @goToAlbumChoosing="handleGoToAlbumChoosing" />
    <AlbumComponent :album="selectedAlbum" @goToAlbumChoosing="handleGoToAlbumChoosing" @selectTrack="handleSelectTrack"
      v-if="appState === AppStates.ChoosingTrack" />
    <AlbumListComponent @selectAlbum="handleSelectAlbum" v-if="appState === AppStates.ChoosingAlbum"
      @uploadNewAlbum="handleUploadNewAlbum" />
    <TrackComponent :track="selectedTrack" :album="selectedAlbum" @goToTrackChoosing="handleGoToTrackChoosing"
      v-if="appState === AppStates.ListeningToTrack" />
  </div>
</template>


<script setup>
import AddAlbumComponent from './components/AddAlbumComponent.vue';
import AlbumComponent from './components/AlbumComponent.vue';
import AlbumListComponent from './components/AlbumListComponent.vue';
import TrackComponent from './components/TrackComponent.vue';
import HeaderComponent from './components/HeaderComponent.vue';


import { onMounted, provide, ref } from 'vue';


const _backendHost = process.env.VUE_APP_BACKEND_HOST || 'localhost';
const _backendPort = process.env.VUE_APP_BACKEND_PORT || 8000;
const backendAddress = `http://${_backendHost}:${_backendPort}`
provide('backendAddress', backendAddress)

const appState = ref(1);

const albums = ref([]);
const selectedAlbum = ref(null); // album object
const selectedTrack = ref(null); // track object

const AppStates = {
  UploadingNewAlbum: 0,
  ChoosingAlbum: 1,
  ChoosingTrack: 2,
  ListeningToTrack: 3,
}

provide('albums', albums)

function handleSelectAlbum(album) {
  selectedAlbum.value = album
  appState.value = AppStates.ChoosingTrack
}

function handleSelectTrack(track) {
  selectedTrack.value = track
  appState.value = AppStates.ListeningToTrack
}

function handleGoToAlbumChoosing() {
  appState.value = AppStates.ChoosingAlbum
}

function handleGoToTrackChoosing() {
  appState.value = AppStates.ChoosingTrack
}

function handleUploadNewAlbum() {
  appState.value = AppStates.UploadingNewAlbum
}

function handleConfirmUploadNewAlbum() {
  appState.value = AppStates.ChoosingAlbum
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

.clickable {
  cursor: pointer;
}
</style>