<template>
  <div class="track-details" v-if="track && album">
    <div @click="$emit('goToTrackChoosing')" class="go-back-button clickable">
      ← <slot>Назад</slot>
    </div>
    <div class="songs-list">
      <div
        v-if="pageState === TrackPageStates.ShowSpinnerInsteadOfLyrics"
        class="marged-spinner"
      >
        <SpinnerComponent size="70px" />
      </div>
      <div v-else>
        <div class="title-and-icons">
          <h2>{{ album.artist.name }} — {{ track.name }}</h2>
          <div class="all-action-icons">
            <FavoriteIconComponent
              :trackId="track.id"
              :isFavorite="track.is_favorite"
              class="favorite-component"
              @toggleIsFavorite="handleToggleIsFavorite"
              title="Мне нравится"
            />
            <div
              class="karaoke-button"
              @click="handleToggleLyricsMode"
              title="Полный текст или кароке-режим"
            >
              <FontAwesomeIcon
                v-if="switchIsInKaraokeMode"
                class="icon-sized-karaoke"
                :icon="faMicrophoneLines"
                fixed-width
              />
              <FontAwesomeIcon
                v-else
                class="icon-sized-karaoke"
                :icon="faFileLines"
                fixed-width
              />
            </div>
            <div
              v-if="track.genius_url"
              class="next-prev-button"
              @click="openLinkInNewTab(track.genius_url)"
            >
              <FontAwesomeIcon
                class="icon-sized"
                :icon="faPenFancy"
                title="Открыть текст на Genius.com"
                fixed-width
              />
            </div>
            <div
              v-if="!isFirstTrack"
              class="next-prev-button"
              @click="goToPreviousTrack"
              title="Предыдущий трек в альбоме"
            >
              <FontAwesomeIcon
                class="icon-sized"
                :icon="faBackwardStep"
                fixed-width
              />
            </div>
            <div
              v-if="!isLastTrack"
              class="next-prev-button"
              @click="goToNextTrack"
              title="Следующий трек в альбоме"
            >
              <FontAwesomeIcon
                :icon="faForwardStep"
                class="icon-sized"
                fixed-width
              />
            </div>
          </div>
        </div>

        <img
          :src="getStaticUrl(album.cover_path)"
          alt="Обложка альбома"
          class="album-cover"
        />

        <div v-if="switchIsInKaraokeMode">
          <button
            v-if="isKaraokeInRecordingMode"
            @click="toggleKaraokeRecordingMode"
            class="karaoke-toggle"
          >
            Назад
          </button>
          <button
            v-if="!karaokeModeIsAvaiable && !isKaraokeInRecordingMode"
            @click="toggleKaraokeRecordingMode"
            class="karaoke-toggle"
          >
            Разметить караоке-текст
          </button>
          <div v-if="isKaraokeInRecordingMode">
            <RecordTimecodesComponent
              :mp3Url="getStaticUrl(track.filename_original)"
              :lyricsText="track.lyrics"
              @sendRecordedKaraokeLyrics="handleUpdatedLyricsKaraoke"
            />
          </div>
          <div v-else>
            <div v-if="karaokeModeIsAvaiable">
              <KaraokeLyricsComponent
                :track="track"
                @goToNextTrack="handleGoToNextTrackFromAutoContinue"
                :autoplay="userSettings.isAutoplayEnabled"
                :autocontinue="userSettings.isAutoplayEnabled"
              />
              <button
                @click="toggleKaraokeRecordingMode"
                class="karaoke-toggle"
              >
                Переразметить караоке-текст
              </button>
              <button @click="removeLyricsKaraoke" class="karaoke-toggle">
                Удалить караоке-текст
              </button>
            </div>
          </div>
        </div>
        <div class="multiline-text" v-else>
          <AudioComponent
            :src="getStaticUrl(track.filename_instrumental)"
            :autoplay="userSettings.isAutoplayEnabled"
            :autocontinue="userSettings.isAutoplayEnabled"
            @goToNextTrack="handleGoToNextTrackFromAutoContinue"
          />
          <AudioComponent
            :src="getStaticUrl(track.filename_vocals)"
            :autoplay="false"
          />
          <AudioComponent
            :src="getStaticUrl(track.filename_original)"
            :autoplay="false"
          />

          {{ track.lyrics }}
          <div class="updateLyricsButtonDiv">
            <div v-if="updateLyricsButtonIsLoading">
              <SpinnerComponent size="20px" />
            </div>
            <button v-else @click="updateLyrics" class="updateLyricsButton">
              Обновить текст
            </button>
          </div>
          <div :style="{ display: 'flex' }">
            <textarea
              v-model="track.notes"
              @input="handleUpdateNotes"
              rows="5"
              class="notes-input"
              placeholder="Добавьте заметки о треке"
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, defineProps, inject, computed, ref, watch } from "vue";
import SpinnerComponent from "./SpinnerComponent.vue";
import KaraokeLyricsComponent from "./KaraokeLyricsComponent.vue";
import RecordTimecodesComponent from "./RecordTimecodesComponent.vue";
import AudioComponent from "./AudioComponent.vue";
import FavoriteIconComponent from "./FavoriteIconComponent.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import {
  faForwardStep,
  faBackwardStep,
  faMicrophoneLines,
  faPenFancy,
} from "@fortawesome/free-solid-svg-icons";
import { faFileLines } from "@fortawesome/free-regular-svg-icons";

const backendAddress = inject("backendAddress");
const getStaticUrl = inject("getStaticUrl");
const updateLyricsButtonIsLoading = ref(false);
const TrackPageStates = {
  ShowSpinnerInsteadOfLyrics: 0,
  ShowPlainLyrics: 1,
  ShowKaraokeLyrics: 2,
  RecordKaraokeLyrics: 3,
};
const userSettings = inject("userSettings");

const pageState = ref(TrackPageStates.ShowSpinnerInsteadOfLyrics);

const props = defineProps({
  selectedTrackId: Number,
  selectedAlbumId: Number,
});

const emit = defineEmits(["goToTrackChoosing", "goToTrackById"]);

const track = ref(null);
const album = ref(null);

const switchIsInKaraokeMode = computed(() => {
  return pageState.value !== TrackPageStates.ShowPlainLyrics;
});

const karaokeModeIsAvaiable = computed(() => {
  return track.value?.lyrics_karaoke;
});

const isKaraokeInRecordingMode = ref(false);

const isFirstTrack = computed(() => track.value.number_in_album == 1);
const isLastTrack = computed(
  () => track.value.number_in_album == album.value.tracks.length
);
const isSingle = computed(() => album.value.tracks.length == 1);

function toggleKaraokeRecordingMode() {
  isKaraokeInRecordingMode.value = !isKaraokeInRecordingMode.value;
}

function handleToggleLyricsMode() {
  if (pageState.value === TrackPageStates.ShowPlainLyrics) {
    pageState.value = TrackPageStates.ShowKaraokeLyrics;
  } else {
    pageState.value = TrackPageStates.ShowPlainLyrics;
  }
}

async function removeLyricsKaraoke() {
  if (window.confirm("Вы уверены, что хотите удалить эту разметку?")) {
    await handleUpdatedLyricsKaraoke(null);
  }
}

async function handleUpdatedLyricsKaraoke(lyrics_karaoke) {
  try {
    pageState.value = TrackPageStates.ShowSpinnerInsteadOfLyrics;
    const response = await fetch(`${backendAddress}/track/${track.value.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lyrics_karaoke: lyrics_karaoke,
      }),
    });
    if (!response.ok) {
      throw new Error("Failed to update karaoke lyrics");
    }
    track.value = await response.json();
    chooseDefaultLyricsPage();
  } catch (error) {
    console.error(error);
    alert("Failed to update karaoke lyrics");
  }
}

async function handleToggleIsFavorite() {
  try {
    const response = await fetch(`${backendAddress}/track/${track.value.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        is_favorite: !track.value.is_favorite,
      }),
    });
    track.value = await response.json();
    if (!response.ok) {
      throw new Error("Failed to update is_favorite");
    }
  } catch (error) {
    console.error(error);
    alert("Failed to update is_favorite");
  }
}

async function handleUpdateNotes() {
  try {
    const response = await fetch(`${backendAddress}/track/${track.value.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        notes: track.value.notes,
      }),
    });
    if (!response.ok) {
      throw new Error("Failed to update notes");
    }
    track.value = await response.json();
  } catch (error) {
    console.error("Error updating notes:", error);
    alert("Failed to update notes");
  }
}

async function updateLyrics() {
  try {
    updateLyricsButtonIsLoading.value = true;
    const response = await fetch(
      `${backendAddress}/tracks/${track.value.id}/lyrics`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      throw new Error("Failed to update lyrics");
    }
    track.value = await response.json();
  } catch (error) {
    console.error(error);
    alert("Failed to update lyrics");
  } finally {
    updateLyricsButtonIsLoading.value = false;
  }
}

function goToNextTrack() {
  // `number_in_album` is indexed from 1
  let nextTrackId = album.value.tracks[track.value.number_in_album + 1 - 1].id;
  emit("goToTrackById", nextTrackId);
}

function goToPreviousTrack() {
  // `number_in_album` is indexed from 1
  let nextTrackId = album.value.tracks[track.value.number_in_album - 1 - 1].id;
  emit("goToTrackById", nextTrackId);
}

function chooseDefaultLyricsPage() {
  if (karaokeModeIsAvaiable.value) {
    pageState.value = TrackPageStates.ShowKaraokeLyrics;
    isKaraokeInRecordingMode.value = false;
  } else {
    pageState.value = TrackPageStates.ShowPlainLyrics;
  }
}

function handleGoToNextTrackFromAutoContinue() {
  if (!isLastTrack.value) {
    goToNextTrack();
  }
}

function openLinkInNewTab(url) {
  window.open(url, "_blank");
}

const fetchAlbum = async () => {
  try {
    const response = await fetch(
      `${backendAddress}/album/${props.selectedAlbumId}`
    );
    if (!response.ok) throw new Error("Failed to fetch");
    album.value = await response.json();
  } catch (error) {
    console.error("Error fetching album:", error);
  }
};

const fetchTrack = async () => {
  try {
    const response = await fetch(
      `${backendAddress}/track/${props.selectedTrackId}`
    );
    if (!response.ok) throw new Error("Failed to fetch");
    track.value = await response.json();
  } catch (error) {
    console.error("Error fetching album:", error);
  }
};

watch(
  () => props.selectedTrackId,
  async () => {
    await fetchTrack();
    chooseDefaultLyricsPage();
  },
  { immediate: true }
);

watch(
  () => props.selectedAlbumId,
  async () => {
    await fetchAlbum();
  },
  { immediate: true }
);
</script>

<style scoped>
.album-cover {
  display: block;
  margin-left: auto;
  margin-right: auto;
  max-width: 300px;
  margin-bottom: 10px;
  margin-top: 10px;
}

.track-details {
  max-width: 800px;
  margin: 10px auto;
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

.multiline-text {
  white-space: pre-wrap;
  font-size: 20px;
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
.title-and-icons {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.all-action-icons {
  display: flex;
  gap: 10px;
}

.marged-spinner {
  margin-top: 50px;
}

.karaoke-toggle {
  padding: 10px 20px;
  margin: 10px 10px 10px 0;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  font-weight: bold;
}

.karaoke-toggle:hover {
  background-color: #e2e6ea;
}

.karaoke-toggle:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.5);
}

.favorite-component {
  position: relative;
  top: 0.1em;
  padding: 0 5px;
}

.next-prev-button {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.icon-sized {
  width: 24px;
  height: 24px;
}

.karaoke-button {
  cursor: pointer;
}

.icon-sized-karaoke {
  width: 24px;
  height: 24px;
}

.notes-input {
  width: 100%;
  padding: 10px 0 0 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  resize: vertical;
}
</style>
