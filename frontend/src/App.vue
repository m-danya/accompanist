<template>
  <div id="app">
    <HeaderComponent
      @goToAlbumChoosing="handleGoToAlbumChoosing"
      @refreshAlbums="fetchAlbums"
    />
    <div v-if="albumsAreLoading" class="spinner-container">
      <SpinnerComponent size="70px" />
    </div>
    <div v-else>
      <AddAlbumComponent
        v-if="appState === AppStates.UploadingNewAlbum"
        @confirmUploadNewAlbum="handleConfirmUploadNewAlbum"
        @goToAlbumChoosing="handleGoToAlbumChoosing"
      />
      <AlbumComponent
        v-if="appState === AppStates.ChoosingTrack"
        :album="selectedAlbum"
        @goToAlbumChoosing="handleGoToAlbumChoosing"
        @selectTrack="handleSelectTrack"
        @deleteAlbum="handleDeleteAlbum"
      />
      <AlbumListComponent
        :albums="albums"
        @selectAlbum="handleSelectAlbum"
        v-if="appState === AppStates.ChoosingAlbum"
        @uploadNewAlbum="handleUploadNewAlbum"
      />
      <TrackComponent
        :track="selectedTrack"
        :album="selectedAlbum"
        @goToTrackChoosing="handleGoToTrackChoosing"
        @goToTrackByNumberInAlbum="handleGoToTrackByNumberInAlbum"
        @refreshAlbums="fetchAlbums"
        v-if="appState === AppStates.ListeningToTrack"
      />
    </div>
  </div>
</template>

<script setup>
import AddAlbumComponent from "./components/AddAlbumComponent.vue";
import AlbumComponent from "./components/AlbumComponent.vue";
import AlbumListComponent from "./components/AlbumListComponent.vue";
import TrackComponent from "./components/TrackComponent.vue";
import HeaderComponent from "./components/HeaderComponent.vue";
import SpinnerComponent from "./components/SpinnerComponent.vue";

import { onMounted, provide, ref, computed } from "vue";

const _backendHost = process.env.VUE_APP_DEPLOYMENT_HOST || "localhost";
const _backendPort = process.env.VUE_APP_BACKEND_PORT || 8090;
const backendAddress = `http://${_backendHost}:${_backendPort}`;

provide("backendAddress", backendAddress);

const albums = ref([]);
const albumsAreLoading = ref(true);

const appState = ref(1);

const selectedAlbumId = ref(null);
const selectedTrackId = ref(null);
const selectedAlbum = computed(() =>
  albums.value.find((album) => album.id === selectedAlbumId.value)
);
const selectedTrack = computed(() =>
  selectedAlbum.value.tracks.find((track) => track.id === selectedTrackId.value)
);

const AppStates = {
  UploadingNewAlbum: 0,
  ChoosingAlbum: 1,
  ChoosingTrack: 2,
  ListeningToTrack: 3,
};

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function handleSelectAlbum(albumId) {
  selectedAlbumId.value = albumId;
  appState.value = AppStates.ChoosingTrack;
  scrollToTop();
}

function handleSelectTrack(trackId) {
  selectedTrackId.value = trackId;
  appState.value = AppStates.ListeningToTrack;
  scrollToTop();
}

function handleGoToAlbumChoosing() {
  appState.value = AppStates.ChoosingAlbum;
  scrollToTop();
}

function handleGoToTrackChoosing() {
  appState.value = AppStates.ChoosingTrack;
  scrollToTop();
}

function handleUploadNewAlbum() {
  appState.value = AppStates.UploadingNewAlbum;
  scrollToTop();
}

function handleConfirmUploadNewAlbum() {
  appState.value = AppStates.ChoosingAlbum;
  scrollToTop();
}

function handleGoToTrackByNumberInAlbum(newNumberInAlbum) {
  let track = selectedAlbum.value.tracks.find(
    (track) => track.number_in_album === newNumberInAlbum
  );
  selectedTrackId.value = track.id;
  scrollToTop();
}

const handleDeleteAlbum = async () => {
  handleGoToAlbumChoosing();
  await fetchAlbums();
};

const fetchAlbums = async () => {
  albumsAreLoading.value = true;
  try {
    const response = await fetch(`${backendAddress}/collection/albums`);
    if (!response.ok) throw new Error("Failed to fetch");
    albums.value = await response.json();
  } catch (error) {
    console.error("Error fetching albums:", error);
  } finally {
    albumsAreLoading.value = false;
  }
};

onMounted(() => {
  fetchAlbums();
});
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

body {
  font-family: "Roboto", sans-serif;
  background-color: #fafafa;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: "Roboto", sans-serif;
}

.clickable {
  cursor: pointer;
}

.spinner-container {
  margin-top: 200px;
}

/* Safari */
@-webkit-keyframes spin {
  0% {
    -webkit-transform: rotate(0deg);
  }

  100% {
    -webkit-transform: rotate(360deg);
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
