<template>
  <div id="app">
    <AddAlbumComponent />
    <AlbumListComponent />
  </div>
</template>

<script>
import AddAlbumComponent from './components/AddAlbumComponent.vue';
import AlbumListComponent from './components/AlbumListComponent.vue';

export default {
  name: 'App',
  components: {
    AddAlbumComponent,
    AlbumListComponent
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

/* Устанавливаем шрифт Roboto для всего приложения */
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
</style>./components/AddAlbumComponent.vue