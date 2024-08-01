import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"
import DrinkPage from "../pages/drink/index.vue"
import OrderPage from "../pages/order/index.vue"
import StorePage from "../pages/store/index.vue"
import ToppingPage from "../pages/topping/index.vue"
import UserPage from "../pages/user/index.vue"
import LoginPage from "../pages/login/index.vue"
import CreateOrderPage from "../pages/createOrder/index.vue"
import NotFound404Page from "../pages/404/index.vue"
declare module 'vue-router' {
    interface RouteMeta {
        isHiddenOnNav?: boolean
        text: string
    }
}
const routesData: RouteRecordRaw[] = [
    {
        path: '/login',
        component: LoginPage,
        name: "login",
        meta: {
            text: "登入"
        }
    },
    {
        path: '/drink',
        component: DrinkPage,
        name: "drink",
        meta: {
            text: "飲料"
        }
    },
    {
        path: '/order',
        component: OrderPage,
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
        component: ToppingPage,
        name: "topping",
        meta: {
            text: "配料"
        }
    },
    {
        path: '/user',
        component: UserPage,
        name: "user",
        meta: {
            text: "用戶"
        }
    },
    {
        path: '/create_order',
        component: CreateOrderPage,
        name: "create_order",
        meta: {
            isHiddenOnNav: true,
            text: "創建訂單"
        }
    },
    {
        path: '/:pathMatch(.*)*',
        component: NotFound404Page,
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

router.onError((err:Error) => { //TODO
    
    console.error("Router error:", err.message);
  });
export { router, routesData }