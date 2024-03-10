<template>
  <div class="container">
    <div class="form-container">
      <h1>Добавить альбом</h1>
      <input v-model="artist" placeholder="Исполнитель">
      <input v-model="songTitle" placeholder="Название альбома">
      <button @click="addSong">Добавить</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      songTitle: '',
      artist: ''
    }
  },
  methods: {
    async addSong() {
      try {
        const response = await axios.post('http://localhost:8000/add_album/', {
          song_title: this.songTitle,
          artist: this.artist
        });
        console.log("Альбом добавлен: " + JSON.stringify(response.data));
      } catch (error) {
        console.error(error);
        alert("Ошибка при добавлении альбома");
      }
    }
  }
}
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

.form-container {
  display: flex;
  flex-direction: column;
  /* align-items: center; */
  text-align: left;
  /* padding: 20px; */
  width: 300px;
}

input {
  margin: 5px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  margin-top: 10px;
  width: 100%;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
