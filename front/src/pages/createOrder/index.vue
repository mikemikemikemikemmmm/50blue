<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { ICE_CONTENT_VALUE_LIST, SUGAR_CONTENT_VALUE_LIST } from '../../const';
import { DrinkApi, OrderItemApi, ToppingApi, OrderApi } from '../../api';
import { useGlobalStore } from '../../store';
export interface OrderItemEditingData extends OrderItemApi.CreateData {
  price: number
}
let toppingData = [] as ToppingApi.GetResponse[]
let drinkData = [] as DrinkApi.GetResponse[]
const fetchDrinkAndTopping = async () => {
  const [allDrink, allTopping] = await Promise.all([DrinkApi.CRUD.getAllApi(), ToppingApi.CRUD.getAllApi()])
  if (allDrink.response && allTopping.response) {
    drinkData = allDrink.response
    toppingData = allTopping.response
    defaultOrderItem.drink_id = drinkData[0]?.id
    defaultOrderItem.price = drinkData[0]?.price
  }
}
onBeforeMount(() => {
  fetchDrinkAndTopping()
})

const orderItemList = ref<OrderItemEditingData[]>([])
const orderTotalPrice = ref<number>(0)
const defaultOrderItem = {
  drink_id: -1,
  topping_ids: [],
  ice_content: ICE_CONTENT_VALUE_LIST[0],
  sugar_content: SUGAR_CONTENT_VALUE_LIST[0],
  price: 0
} as OrderItemEditingData

const handleOrderTotalPrice = () => {
  orderTotalPrice.value = orderItemList.value.reduce((sum, orderItem) => sum + orderItem.price, 0)
}
const handleCreateNewOrderItem = () => {
  if (drinkData.length === 0) {
    const store = useGlobalStore()
    store.createAlertData({ type: "error", text: "無飲品資料" })
    return
  }
  orderItemList.value.push({ ...defaultOrderItem, topping_ids: [] })
  handleOrderTotalPrice()
}
const handleDeleteOrderItem = (index: number) => {
  orderItemList.value.splice(index, 1)
  handleOrderTotalPrice()
}
const handleSelectDrinkId = (seletedDrinkId: number, index: number) => {
  const target = orderItemList.value[index]
  target.drink_id = seletedDrinkId
  target.price = calculateItemPrice(target.drink_id, target.topping_ids)
  handleOrderTotalPrice()
}
const handleSelectToppingIds = (seletedToppingIds: number[], index: number) => {
  const target = orderItemList.value[index]
  target.topping_ids = seletedToppingIds
  target.price = calculateItemPrice(target.drink_id, target.topping_ids)
  handleOrderTotalPrice()
}
const handleSubmit = async () => {
  if (orderItemList.value.length === 0) {
    return
  }
  const { error } = await OrderApi.createApi(orderItemList.value)
  if (error) {
    return
  }
  orderItemList.value = []
  handleOrderTotalPrice()
}
const calculateItemPrice = (drinkId: number, toppingIds: number[]) => {
  const targetDrink = drinkData.find(d => d.id === drinkId)
  if (!targetDrink) {
    throw Error("找不到飲品")
  }
  const targetToppings = toppingData.filter(t => toppingIds.includes(t.id))
  if (targetToppings.length !== toppingIds.length) {
    throw Error("找不到配料")
  }
  return targetDrink.price + targetToppings.reduce((sum, item) => sum + item.price, 0)
} 
</script>

<template>
  <v-container>
    <v-list density="compact">
      <v-list-item>
        <div class="d-flex">
          <span>
            總價:{{ orderTotalPrice }}
          </span>
          <v-btn class="ml-auto" variant="outlined" @click="handleCreateNewOrderItem">
            新增單項
          </v-btn>
          <v-btn class="mx-2" variant="outlined" @click="handleSubmit">
            送出訂單
          </v-btn>
        </div>
      </v-list-item>
      <v-list-item v-for="(orderItem, index) in orderItemList">
        <v-row density="compact">
          <v-col sm="2">
            <v-select @update:model-value="seletedDrinkId => handleSelectDrinkId(seletedDrinkId, index)"
              :model-value="orderItem.drink_id" :item-value="'id'" :item-title="'name'" density="compact"
              :hide-details="true" label="飲品" :items="drinkData" />
          </v-col>
          <v-col sm="3">
            <v-select @update:model-value="seletedToppingIds => handleSelectToppingIds(seletedToppingIds, index)"
              :model-value="orderItem.topping_ids" :item-value="'id'" :item-title="'name'" density="compact"
              :hide-details="true" label="配料" multiple :items="toppingData" />
          </v-col>
          <v-col sm="2">
            <v-select v-model="orderItem.sugar_content" density="compact" :hide-details="true" label="糖度"
              :items="SUGAR_CONTENT_VALUE_LIST" />
          </v-col>
          <v-col sm="2">
            <v-select v-model="orderItem.ice_content" density="compact" :hide-details="true" label="冰塊"
              :items="ICE_CONTENT_VALUE_LIST" />
          </v-col>
          <v-col sm="2">
            <span :style="{ display: 'flex', alignItems: 'center', height: '100%' }">
              價格:{{ orderItem.price }}
            </span>
          </v-col>
          <v-col sm="1">
            <v-icon class="all-item-center" size="small" @click="handleDeleteOrderItem(index)">
              mdi-delete
            </v-icon>
          </v-col>
        </v-row>
      </v-list-item>
    </v-list>
  </v-container>
</template>
