<template>
  <div class="track-details">
    <div @click="$emit('goToTrackChoosing')" class="go-back-button clickable">
      ← <slot>Назад</slot>
    </div>
    <h2>{{ track.name }} by {{ album.artist.name }}</h2>
    <img
      :src="getStaticUrl(album.cover_path)"
      alt="Обложка альбома"
      class="album-cover"
    />
    <div class="songs-list">
      <audio controls>
        <source
          :src="getStaticUrl(track.filename_instrumental)"
          type="audio/mpeg"
        />
      </audio>
      <audio controls>
        <source :src="getStaticUrl(track.filename_vocals)" type="audio/mpeg" />
      </audio>

      <div class="navigation-buttons">
        <button
          v-if="!isFirstTrack"
          @click="$emit('goToTrackByNumberInAlbum', track.number_in_album - 1)"
        >
          Предыдущий трек
        </button>
        <button
          v-if="!isLastTrack"
          @click="$emit('goToTrackByNumberInAlbum', track.number_in_album + 1)"
        >
          Следующий трек
        </button>
      </div>

      <div class="multiline-text">
        {{ track.lyrics }}
      </div>
      <div class="updateLyricsButtonDiv">
        <div v-if="updateLyricsButtonIsLoading">
          <SpinnerComponent size="20px" />
        </div>
        <button v-else @click="updateLyrics" class="updateLyricsButton">
          Обновить текст
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { defineEmits, defineProps, inject, computed, ref } from "vue";
import SpinnerComponent from "./SpinnerComponent.vue";

const backendAddress = inject("backendAddress");
const updateLyricsButtonIsLoading = ref(false);
const props = defineProps({
  track: Object,
  album: Object,
});

const emit = defineEmits([
  "goToTrackChoosing",
  "goToTrackByNumberInAlbum",
  "refreshAlbums",
]);

const getStaticUrl = (filename) => {
  return `${backendAddress}/static/${filename}`;
};

async function updateLyrics() {
  try {
    updateLyricsButtonIsLoading.value = true;
    const response = await fetch(
      `${backendAddress}/collection/update_lyrics/${props.track.id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    emit("refreshAlbums");
    if (!response.ok) {
      throw new Error("Failed to update lyrics");
    }
  } catch (error) {
    console.error(error);
    alert("Failed to update lyrics");
  } finally {
    updateLyricsButtonIsLoading.value = false;
  }
}

const isFirstTrack = computed(() => props.track.number_in_album == 1);
const isLastTrack = computed(
  () => props.track.number_in_album == props.album.tracks.length
);
</script>

<style scoped>
.album-cover {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 40px;
  max-width: 300px;
}

.track-details {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  background-color: white;
}

.track-details h2 {
  color: #343a40;
  margin-bottom: 16px;
  text-align: center;
}

.songs-list ul {
  list-style-type: none;
  padding: 0;
  margin-top: 0;
}

.songs-list li {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.song-title {
  font-weight: bold;
  color: #495057;
  margin-bottom: 5px;
}

.song-duration {
  font-style: italic;
  color: #6c757d;
  margin-bottom: 10px;
}

.song-info {
  display: flex;
  align-items: center;
  /* This will vertically center align the items if they have different heights */
  justify-content: space-between;
  /* Adjusts the space between the child elements */
}

.multiline-text {
  white-space: pre-wrap;
  font-size: 20px;
}

audio {
  width: 100%;
  margin-top: 10px;
}

.navigation-buttons {
  display: flex;
  justify-content: center;
  gap: 10px; /* Adjust the gap between buttons as needed */
  margin: 20px 0; /* Adjust spacing as needed */
}

.navigation-buttons button {
  cursor: pointer;
  padding: 10px 15px;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.updateLyricsButtonDiv {
  margin: 20px 0;
}
.updateLyricsButton {
  cursor: pointer;
  padding: 10px 15px;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 5px;
  transition: background-color 0.2s;
}
</style>
