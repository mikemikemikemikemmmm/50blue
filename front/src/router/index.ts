import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"
import { hasToken, removeToken, removeTokenAndRedirectToLogin } from "../utils"
import { checkTokenWhenFristEnterApi } from "../api/auth"
import { useGlobalStore } from "../store"
declare module 'vue-router' {
    interface RouteMeta {
        isHiddenOnNav?: boolean
        text: string
    }
}
const routesData: RouteRecordRaw[] = [
    {
        path: '/login',
        component: () => import("../pages/login/index.vue"),
        name: "login",
        meta: {
            text: "登入"
        }
    },
    {
        path: '/drink',
        component: () => import("../pages/drink/index.vue"),
        name: "drink",
        meta: {
            text: "飲料"
        }
    },
    {
        path: '/order',
        component: () => import("../pages/order/index.vue"),
        name: "order",
        meta: {
            text: "訂單"
        }
    },
    // {
    //     path: '/store',
    //     component: StorePage,
    //     name: "store",
    //     meta: {
    //         text: "店面"
    //     }
    // },
    {
        path: '/topping',
        component: () => import("../pages/topping/index.vue"),
        name: "topping",
        meta: {
            text: "配料"
        }
    },
    {
        path: '/user',
        component: () => import("../pages/user/index.vue"),
        name: "user",
        meta: {
            text: "用戶"
        }
    },
    {
        path: '/create_order',
        component: () => import("../pages/createOrder/index.vue"),
        name: "create_order",
        meta: {
            isHiddenOnNav: true,
            text: "創建訂單"
        }
    },
    {
        path: '/:pathMatch(.*)*',
        component: () => import("../pages/404/index.vue"),
        name: "not_found",
        meta: {
            isHiddenOnNav: true,
            text: "404"
        }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes: routesData,
})

router.onError((err: Error) => {
    console.error("Router error:", err.message);
});
router.beforeEach(async (to, from) => {
    const isToLogin = to.name === 'login'
    if (hasToken()) {
        const { response } = await checkTokenWhenFristEnterApi()
        if (response) {
            const isTokenLegal = response.is_token_legal
            const store = useGlobalStore()
            if (isTokenLegal) {
                store.setAllowRouteNameList(response.allow_route_name_list)
                if (isToLogin) {
                    return { name: response.allow_route_name_list[0] }
                } else {
                    return true
                }
            } else {
                removeToken()
                return { name: 'login' }
            }
        } else {
            return { name: 'login' }
        }
    } else {
        if (isToLogin) {
            return true
        }
        return { name: 'login' }
    }
})
export { router, routesData }