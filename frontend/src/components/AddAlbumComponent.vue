<template>
  <div>
    <h1>Добавить альбом</h1>
    <input v-model="artist" placeholder="Исполнитель">
    <input v-model="songTitle" placeholder="Название альбома">
    <button @click="addSong">Добавить</button>
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
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

input {
  margin: 5px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 250px;
}

button {
  margin-top: 10px;
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
