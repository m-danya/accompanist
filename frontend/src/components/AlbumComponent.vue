<template>
    <div class="album-details">
        <h2>{{ album.name }} by {{ album.artist.name }}</h2>
        <img :src="getStaticUrl(album.cover_path)" alt="Обложка альбома" class="album-cover">
        <div class="songs-list">
            <ul>
                <li v-for="track in album.tracks" :key="track.id">
                    <div class="song-title">{{ track.name }}</div>
                    <div class="song-duration">Длительность: {{ track.duration }}</div>
                    <audio controls>
                        <source :src="getStaticUrl(track.filename_instrumental)" type="audio/mpeg">
                    </audio>
                    <audio controls>
                        <source :src="getStaticUrl(track.filename_vocals)" type="audio/mpeg">
                    </audio>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { defineProps, inject } from 'vue';


const backendAddress = inject('backendAddress')

const props = defineProps({
    album: Object
});

const getStaticUrl = (filename) => {
    return `${backendAddress}/static/${filename}`;
};
</script>

<style scoped>
.album-cover {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

.album-details {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
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

audio {
    width: 100%;
    margin-top: 10px;
}
</style>
