<template>
  <div id="app">
    <AddAlbumComponent />
    <AlbumListComponent />
  </div>
</template>


<script setup>
import AddAlbumComponent from './components/AddAlbumComponent.vue';
import AlbumListComponent from './components/AlbumListComponent.vue';


const _backendHost = process.env.VUE_APP_BACKEND_HOST || 'localhost';
const _backendPort = process.env.VUE_APP_BACKEND_PORT || 8000;
const backendAddress = `http://${_backendHost}:${_backendPort}`
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
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