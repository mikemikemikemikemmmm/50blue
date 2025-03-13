<script setup lang="ts">
import { RouterView } from 'vue-router';

import NavComponent from "./components/nav.vue"
import Loading from "./components/loading.vue"
import AlertContainer from "./components/alertContainer.vue"
</script>

<template>
  <v-app style="position: relative;">
    <Loading />
    <NavComponent />
    <AlertContainer />
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>
