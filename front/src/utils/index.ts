import { TOKEN_KEY_IN_LOCALSTORAGE } from "../const";
import { useGlobalStore } from "../store";
import { router } from "../router";

export const hasToken = () => {
    return !!localStorage.getItem(TOKEN_KEY_IN_LOCALSTORAGE)
}

export const removeToken = () => {
    localStorage.removeItem(TOKEN_KEY_IN_LOCALSTORAGE)
    const store = useGlobalStore()
    store.setHasTokenRef(hasToken())
}

export const getToken = () => localStorage.getItem(TOKEN_KEY_IN_LOCALSTORAGE);
export const setToken = (token: string) => {
    localStorage.setItem(TOKEN_KEY_IN_LOCALSTORAGE, token)
    const store = useGlobalStore()
    store.setHasTokenRef(hasToken())
}

export const removeTokenAndRedirectToLogin = () => {
    const store = useGlobalStore()
    removeToken()
    store.setAllowRouteNameList(["login"])
    router.push({ name: "login" })
}

export const inputRules = {
    requiredString(value: string): string | boolean {
        if (value?.length > 0) {
            return true;
        }
        return '此欄位為必須';
    },
    requiredPositiveInt(value: string): string | boolean {
        const numVal = Number(value)
        if (Number.isInteger(numVal) && numVal > 0) {
            return true;
        }
        return '須為正整數';
    },
};

export const formatOrderItemToppingList = (toppingList: string[]) => {
    return toppingList.length === 0 ? "無配料" : toppingList.join("、")

}