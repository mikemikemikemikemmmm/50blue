<script setup lang="ts">
import { RouteRecordRaw, useRouter } from "vue-router";
import { computed, ref, watch } from 'vue';

import { routesData } from "../router"
import { useGlobalStore } from "../store";
import { removeTokenAndRedirectToLogin } from "../utils";
const store = useGlobalStore()
const router = useRouter()

const isShowDrawer = ref(false)
const currentPageName = ref<string>(router.currentRoute.value.meta.text as string)
watch(
    () => router.currentRoute.value,
    currentRoute => {
        currentPageName.value = currentRoute.meta.text
    },
    { immediate: true }
)

const allowRouteList = computed(() => {
    const result = [] as RouteRecordRaw[]
    store.allowRouteNameList.forEach(routeName => {
        const target = routesData.find(r => r.name === routeName)
        if (target) {
            result.push(target)
        }
    })
    return result
})

const handleClickLogout = () => {
    removeTokenAndRedirectToLogin()
}
const handleCreateOrder = () => {
    router.push("/create_order")
}

</script>

<template>
    <v-app-bar color="primary" prominent>
        <template v-slot:prepend>
            <v-app-bar-nav-icon variant="text" @click.stop="isShowDrawer = !isShowDrawer"></v-app-bar-nav-icon>
        </template>
        <v-app-bar-title>{{ currentPageName }}</v-app-bar-title>
        <template v-slot:append v-if="store.hasTokenRef">
            <v-btn @click="handleCreateOrder">
                創建訂單
            </v-btn>
            <v-btn @click="handleClickLogout">
                登出
            </v-btn>
        </template>
    </v-app-bar>
    <v-navigation-drawer v-model="isShowDrawer" :width="100" temporary>
        <v-list>
            <v-list-item :to="route.path" :style="{
                display: route.meta?.isHiddenOnNav ? 'none' : 'block',
                textAlign: 'center'
            }" :key="route.path" v-for="route in allowRouteList">
                {{ route.meta?.text || "" }}
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>
