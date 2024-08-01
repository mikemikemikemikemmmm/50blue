<script setup lang="ts">
import { useGlobalStore } from '../store';
const store = useGlobalStore()
</script>
<template>
    <div v-if="store.isLoading" :style="{
        maxWidth: '50%',
        position: 'absolute',
        left: '10px',
        bottom: '10px',
        zIndex: 99
    }">
        <v-alert class="my-1" density="compact" type="info" :icon="false">
            <v-progress-circular  color="white" indeterminate />
            <span :style="{ marginLeft: '10px'}">loading...</span>
        </v-alert>
    </div>
</template>