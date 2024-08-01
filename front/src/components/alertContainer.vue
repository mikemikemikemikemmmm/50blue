<script setup lang="ts">
import { useGlobalStore } from '../store';
const store = useGlobalStore()
</script>
<template>
    <div :style="{
        position: 'absolute', right: '10px', bottom: '10px', zIndex: 99, maxWidth:'50%' }">
        <v-alert class="my-1" v-for="alert in store.alertData" :key="alert.timestamp" density="compact"
            :type="alert.type" :text="alert.text" />
    </div>
</template>