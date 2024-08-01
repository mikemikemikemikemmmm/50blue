import { BaseApi } from "../api"
import { StoreType, useGlobalStore } from "../store"

export const errorHandler = (error: BaseApi.ErrorResponseData, store?: StoreType) => {
    const _store = store || useGlobalStore()
    _store.createAlertData({
        type: "error",
        text: error?.response?.data?.detail || error.message || "不明錯誤"
    })
}