<template>
  <v-container style="display: flex;justify-content: center;">
    <v-table class="text-center" density="compact">
      <thead>
        <tr>
          <th class="text-center">
            創建日期
          </th>
          <th class="text-center">
            價格
          </th>
          <th class="text-center">
            飲品
          </th>
          <th class="text-center">
            冰量
          </th>
          <th class="text-center">
            糖量
          </th>
          <th class="text-center">
            配料
          </th>
        </tr>
      </thead>
      <tbody>
        <order-item-row v-for="orderItem in orderItemDataList" :order-data="orderItem" :key="orderItem.id" />
      </tbody>
    </v-table>
  </v-container>
</template>

<script setup lang="ts">
import OrderItemRow from "./row.vue"
import { onBeforeMount, ref } from 'vue'
import { OrderApi } from '../../api';
const orderItemDataList = ref<OrderApi.GetResponse[]>([])
const fetchData = async () => {
  const { response } = await OrderApi.getAllApi()
  if (response) {
    orderItemDataList.value = response
  }
}
onBeforeMount(() => {
  fetchData()
})
</script>
