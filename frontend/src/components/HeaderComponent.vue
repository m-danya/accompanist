<template>
    <header class="header clickable">
        <img :src="logo" alt="Accompanist Logo" class="logo">
        <h1>Accompanist</h1>
    </header>
</template>

<script setup>
import { ref } from 'vue';

const logo = ref(new URL('@/assets/logo.png', import.meta.url).href);
</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    padding: 30px 0 0 50px;
}

.logo {
    width: 50px;
    /* Adjust based on your logo's size */
    height: auto;
    margin-right: 10px;
}

h1 {
    margin: 0;
    font-size: 24px;
    /* Adjust based on your preference */
}
</style>