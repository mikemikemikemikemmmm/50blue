import { defineStore } from "pinia"
import { reactive, ref } from "vue"
import { hasToken } from "../utils"
interface AlertCreateData {
  type: "success" | "info" | "warning" | "error",
  text: string
}
interface Alert extends AlertCreateData {
  timestamp: number
}

export const useGlobalStore = defineStore('globalStore', () => {
  //route name
  const defaultAllowRoute = "login"
  const allowRouteNameList = ref<string[]>([defaultAllowRoute])
  function setAllowRouteNameList(list: string[]) {
    allowRouteNameList.value = [...list, "not_found"]
  }

  //alert
  const deleteSelfSecond = 3
  const maxLength = 5
  const alertData = reactive<Alert[]>([])
  const createAlertData = (alert: AlertCreateData) => {
    const newItem = { ...alert, timestamp: Date.now() }
    if (alertData.length >= maxLength) {
      alertData.splice(0, 1)
    }
    alertData.push(newItem)
    setTimeout(() => {
      deleteAlertByTimestamp(newItem.timestamp)
    }, 1000 * deleteSelfSecond)
  }
  const deleteAlertByTimestamp = (timestamp: number) => {
    const targetIndex = alertData.findIndex(a => a.timestamp === timestamp)
    if (targetIndex !== -1) {
      alertData.splice(targetIndex, 1);
    }
  }

  //loading
  const isLoading = ref(false)
  const setIsLoading = (val: boolean) => {
    if (val === isLoading.value) {
      return
    }
    isLoading.value = val
  }

  //token
  const hasTokenRef = ref(hasToken())
  const setHasTokenRef = (val: boolean) => {
    hasTokenRef.value = val
  }
  return { setHasTokenRef, hasTokenRef, isLoading, setIsLoading, alertData, createAlertData, deleteAlertByTimestamp, setAllowRouteNameList, allowRouteNameList }
})
export type StoreType = ReturnType<typeof useGlobalStore>