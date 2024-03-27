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
      <div v-if="pageState === TrackPageStates.ShowSpinnerInsteadOfLyrics">
        <SpinnerComponent size="70px" />
      </div>
      <div v-else>
        <div class="switch-outer-container">
          <div class="switch-container">
            <input
              id="karaoke-switch"
              type="checkbox"
              v-model="switchIsInKaraokeMode"
              @change="handleToggleLyricsMode"
            />
            <label for="karaoke-switch" class="switch-label">
              <span class="switch-label-text" v-if="switchIsInKaraokeMode"
                >Режим караоке</span
              >
              <span class="switch-label-text" v-else>Полный текст</span>
            </label>
          </div>
        </div>
        <div class="navigation-buttons" v-if="!isSingle">
          <button
            v-if="!isFirstTrack"
            @click="
              $emit('goToTrackByNumberInAlbum', track.number_in_album - 1)
            "
          >
            Предыдущий трек
          </button>
          <button
            v-if="!isLastTrack"
            @click="
              $emit('goToTrackByNumberInAlbum', track.number_in_album + 1)
            "
          >
            Следующий трек
          </button>
        </div>

        <div v-if="switchIsInKaraokeMode">
          <div v-if="karaokeModeIsAvaiable">
            <KaraokeLyricsComponent :track="props.track" />
          </div>
          <div v-else>
            Для этого трека ещё не записана информация о таймингах.

            <!-- <button
              @click="
                ...
              "
            >
              Записать
            </button> -->
            <RecordTimecodesComponent
              :mp3Url="getStaticUrl(track.filename_original)"
              :lyricsText="track.lyrics"
              @sendRecordedKaraokeLyrics="handleUpdatedLyricsKaraoke"
            />
          </div>
        </div>
        <div class="multiline-text" v-else>
          <AudioComponent
            :src="getStaticUrl(track.filename_instrumental)"
            :autoplay="userSettings.isAutoplayEnabled"
            :autocontinue="userSettings.isAutoplayEnabled"
            @finishAudio="
              () => {
                if (!isLastTrack) {
                  $emit('goToTrackByNumberInAlbum', track.number_in_album + 1);
                }
              }
            "
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
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import {
  defineEmits,
  defineProps,
  inject,
  computed,
  ref,
  onMounted,
  watch,
} from "vue";
import SpinnerComponent from "./SpinnerComponent.vue";
import KaraokeLyricsComponent from "./KaraokeLyricsComponent.vue";
import RecordTimecodesComponent from "./RecordTimecodesComponent.vue";
import AudioComponent from "./AudioComponent.vue";

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

const switchIsInKaraokeMode = computed(() => {
  return pageState.value !== TrackPageStates.ShowPlainLyrics;
});

const karaokeModeIsAvaiable = computed(() => {
  return props.track.lyrics_karaoke;
});

function handleToggleLyricsMode() {
  if (pageState.value === TrackPageStates.ShowPlainLyrics) {
    pageState.value = TrackPageStates.ShowKaraokeLyrics;
  } else {
    pageState.value = TrackPageStates.ShowPlainLyrics;
  }
}

async function handleUpdatedLyricsKaraoke(lyrics_karaoke) {
  try {
    pageState.value = TrackPageStates.ShowSpinnerInsteadOfLyrics;
    const response = await fetch(
      `${backendAddress}/collection/update_lyrics_karaoke/${props.track.id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          lyrics_karaoke: lyrics_karaoke,
        }),
      }
    );
    emit("refreshAlbums");
    if (!response.ok) {
      throw new Error("Failed to update karaoke lyrics");
    }
  } catch (error) {
    console.error(error);
    alert("Failed to update karaoke lyrics");
  } finally {
    // updateLyricsButtonIsLoading.value = false;
  }
}

const props = defineProps({
  track: Object,
  album: Object,
});

const emit = defineEmits([
  "goToTrackChoosing",
  "goToTrackByNumberInAlbum",
  "refreshAlbums",
]);

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
const isSingle = computed(() => props.album.tracks.length == 1);

function openLyricsPage() {
  if (karaokeModeIsAvaiable.value) {
    pageState.value = TrackPageStates.ShowKaraokeLyrics;
  } else {
    pageState.value = TrackPageStates.ShowPlainLyrics;
  }
}

// open corresponding lyrics page (plain text / karaoke mode) on track changing
watch(
  () => props.track,
  (newTrack, oldTrack) => {
    openLyricsPage();
  }
);

onMounted(() => {
  openLyricsPage();
});
</script>

<style scoped>
.album-cover {
  display: block;
  margin-left: auto;
  margin-right: auto;
  /* margin-bottom: 40px; */
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
.switch-outer-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}
.switch-container {
  position: relative;
  display: inline-block;
  width: 200px;
  height: 34px;
}

.switch-label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.6s;
  border-radius: 34px;
  /* padding: 0 10px; */
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  font-weight: bold;
}

#karaoke-switch:checked + .switch-label {
  background-color: #2196f3;
}

#karaoke-switch {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-label-text {
  margin: 0 auto;
}
</style>
