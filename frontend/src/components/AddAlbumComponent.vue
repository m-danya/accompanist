<template>
  <div class="container">
    <div class="form-container">
      <h1>Добавить альбом</h1>
      <input v-model="searchQuery" placeholder="Исполнитель и название">
      <button @click="addSong">Добавить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';

const backendAddress = inject('backendAddress');
const searchQuery = ref('');

async function addSong() {
  try {
    const response = await fetch(`${backendAddress}/collection/album/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        search_query: searchQuery.value,
      }),
    });
    if (!response.ok) {
      throw new Error('Failed to add album');
    }
    const data = await response.json();
    console.log("Запрос на добавление альбома принят: " + JSON.stringify(data));
    searchQuery.value = ""
  } catch (error) {
    console.error(error);
    alert("Ошибка при добавлении альбома");
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
  text-align: left;
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
