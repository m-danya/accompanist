<template>
  <div class="album-details">
    <div @click="$emit('goToAlbumChoosing')" class="go-back-button clickable">
      ← <slot>Назад</slot>
    </div>
    <h2>{{ album.name }} by {{ album.artist.name }}</h2>
    <img :src="getStaticUrl(album.cover_path)" alt="Обложка альбома" class="album-cover" />
    <div class="songs-list">
      <ul>
        <li
          v-for="track in album.tracks"
          :key="track.id"
          @click="$emit('selectTrack', track.id)"
          :class="{ 'has-karaoke-lyrics': track.lyrics_karaoke }"
        >
          <div class="song-info">
            <div class="song-title clickable">
              <button
                class="favorite-button"
                :class="{ 'is-favorite': track.is_favorite }"
                @click.stop="handleToggleIsFavorite(track)"
              >
                <FontAwesomeIcon class="favorite-icon" :icon="faHeart" />
              </button>
              {{ track.name }}
            </div>
            <div class="song-duration">{{ track.duration }}</div>
          </div>
        </li>
      </ul>
    </div>
    <button @click="deleteAlbum" class="delete-album-button">Удалить альбом</button>
  </div>
</template>

<script setup>
import { defineProps, inject, defineEmits } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faHeart } from "@fortawesome/free-solid-svg-icons";

const backendAddress = inject("backendAddress");

const props = defineProps({
  album: Object,
});

const emit = defineEmits(["selectTrack", "goToAlbumChoosing", "deleteAlbum", "refreshAlbums"]);

const deleteAlbum = async () => {
  if (window.confirm("Вы уверены, что хотите удалить этот альбом?")) {
    try {
      const response = await fetch(`${backendAddress}/collection/album/${props.album.id}`, {
        method: "DELETE",
      });
      if (response.ok) {
        emit("deleteAlbum");
      } else {
        alert("Произошла ошибка при удалении альбома.");
      }
    } catch (error) {
      console.error("Ошибка при удалении альбома:", error);
      alert("Произошла ошибка при удалении альбома.");
    }
  }
};

async function handleToggleIsFavorite(track) {
  try {
    const response = await fetch(`${backendAddress}/collection/update_favorite/${track.id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        is_favorite: !track.is_favorite,
      }),
    });
    emit("refreshAlbums");
    if (!response.ok) {
      throw new Error("Failed to update is_favorite");
    }
  } catch (error) {
    console.error(error);
    alert("Failed to update is_favorite");
  }
}

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
  max-width: 300px;
}

.album-details {
  max-width: 800px;
  margin: 20px auto;
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
  padding: 10px 30px 10px 10px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.song-title {
  font-weight: bold;
  color: #495057;
  /* margin-bottom: 5px; */
  display: flex;
  align-items: center;
  justify-content: start; /* Ensures content is aligned to the start */
  width: 100%; /* Ensures the .song-title takes full width of its parent for better alignment */
}

.song-duration {
  font-style: italic;
  color: #6c757d;
}

.song-info {
  display: flex;
  align-items: center;
  /* This will vertically center align the items if they have different heights */
  justify-content: space-between;
  /* Adjusts the space between the child elements */
}

.has-karaoke-lyrics {
  background-color: #e9f5db; /* A light green background for karaoke tracks */
  border-left: 4px solid #4caf50; /* A green border on the left for emphasis */
  padding-left: 26px; /* Adjust padding to accommodate the border */
}

.song-info:hover .favorite-button,
.favorite-button.is-favorite {
  opacity: 1;
}

.favorite-button {
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s ease;
  padding: 0 15px 0 15px; /* Adds padding to the left and right */
  display: inline-flex; /* Helps maintain alignment with the icon */
  align-items: center; /* Centers the icon vertically */
  justify-content: center; /* Centers the icon horizontally */
}

.favorite-icon {
  color: #db4c4c;
}

audio {
  width: 100%;
  margin-top: 10px;
}

.delete-album-button {
  background-color: #c0392b;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.delete-album-button:hover {
  background-color: darkred;
}

.song-title,
.favorite-button,
.favorite-icon {
  height: 20px; /* Adjust as needed */
  line-height: 20px; /* Adjust to match the height for vertical centering */
  margin-top: -0.15em;
}
.favorite-icon {
  align-self: center; /* Ensures the icon itself is centered within the flex container */
}
</style>
