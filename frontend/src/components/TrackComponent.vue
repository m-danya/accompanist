<template>
  <div class="album-details">
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

      <div class="multiline-text">
        {{ track.lyrics }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, inject, defineEmits } from "vue";

const backendAddress = inject("backendAddress");

const props = defineProps({
  track: Object,
  album: Object,
});

const emit = defineEmits(["goToTrackChoosing"]);

const getStaticUrl = (filename) => {
  return `${backendAddress}/static/${filename}`;
};
</script>

<style scoped>
.album-cover {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 40px;
  max-width: 512px;
}

.album-details {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  background-color: white;
}

.album-details h2 {
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
</style>
