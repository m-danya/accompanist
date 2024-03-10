<template>
  <div class="container">
    <div class="album-list">
      <h1>Доступные альбомы</h1>
      <div class="albums-grid">
        <div class="album" v-for="album in albums" :key="album.id">
          <img :src="album.coverUrl" alt="Обложка альбома" class="album-cover">
          <div class="album-title">{{ album.title }}</div>
          <div class="album-artist">{{ album.artist }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      albums: [
        {
          id: 1,
          title: 'Гранатовый альбом',
          artist: 'Сплин',
          coverUrl: 'https://lh3.googleusercontent.com/ewysufFgQuuht8YmMBUt6kPHHTQfp1juQfXi80eieUOI_j3HKM7fnJxt-PHRZHTLKp7aWa2TcWAgaFgY=w544-h544-l90-rj'
        },
        {
          id: 2,
          title: '7',
          artist: 'Нервы',
          coverUrl: 'https://lh3.googleusercontent.com/IXvEtokz0aEMlbUudmxbosHXyindMk41EKBkk_uZiwRquVOXdoz58SWt8yo2ZZaDZua1zSmMAXEoWO2n=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        }, {
          id: 3,
          title: 'Tragic City',
          artist: 'ЛСП',
          coverUrl: 'https://lh3.googleusercontent.com/jGzUjV9irr8Lyi_PoU7vWaMV3PJtxZGmhRpf1_KQSYM2TaANhItCyawvYIOlY-BiIbcX5aWbRKwyIQ=w544-h544-l90-rj'
        },
      ]
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

.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  justify-items: center;
  /* Центрирует содержимое ячеек по горизонтали */
}

.album {
  display: flex;
  flex-direction: column;
  align-items: start;
  /* Aligns items to the start of the container (left) */
}

.album-cover {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
  /* Adds space between the image and the text */
}

.album-title {
  font-size: 16px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 5px;
}

.album-artist {
  font-size: 14px;
  text-align: left;
  /* Aligns text to the left */
}
</style>