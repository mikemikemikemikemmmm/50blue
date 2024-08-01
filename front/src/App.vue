<script setup lang="ts">
import { onBeforeMount } from "vue";
import NavComponent from "./components/nav.vue"
import Loading from "./components/loading.vue"
import AlertContainer from "./components/alertContainer.vue"
import { RouterView, useRoute, useRouter } from 'vue-router';
import { checkTokenWhenFristEnterApi } from "./api/auth";
import { useGlobalStore } from "./store";
import { hasToken, removeTokenAndRedirectToLogin } from "./utils";
const store = useGlobalStore()
const route = useRoute()
const router = useRouter()
onBeforeMount(async () => {
  const isAtLoginPage = route.name === "login"
  if (hasToken()) {
    const { response } = await checkTokenWhenFristEnterApi()
    if (response) {
      const isTokenLegal = response.is_token_legal
      if (isTokenLegal) {
        store.setAllowRouteNameList(response.allow_route_name_list)
        if (isAtLoginPage) {
          router.push({ name: response.allow_route_name_list[0] })
        }
      } else {
        removeTokenAndRedirectToLogin()
      }
      return
    }
  }
  if (!isAtLoginPage) {
    router.push({ name: "login" })
  }
})
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
