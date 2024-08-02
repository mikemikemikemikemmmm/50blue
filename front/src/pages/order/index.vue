<template>
  <v-container style="display: flex;justify-content: center;">
    <v-table class="text-center" density="compact">
      <template v-slot:top>
        <v-dialog v-model="isShowDeleteDialog" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">確定要刪除{{ deletedRowId }}嗎?</v-card-title>
            <v-card-actions>
              <v-spacer />
              <v-btn color="blue-darken-1" variant="text" @click="handleCloseDeleteDialog">取消</v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="handleConfirmDelete">刪除</v-btn>
              <v-spacer />
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
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
          <th class="text-center">
            刪除
          </th>
        </tr>
      </thead>
      <tbody>
        <order-item-row @handle-delete-order="handleDeleteOrder" v-for="orderItem in orderItemDataList"
          :order-data="orderItem" :key="orderItem.id" />
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

const deletedRowId = ref(-1)
const isShowDeleteDialog = ref(false)
const handleDeleteOrder = (data:{id: number}) => {
  deletedRowId.value = data.id
  isShowDeleteDialog.value = true
}
const handleCloseDeleteDialog = () => {
  deletedRowId.value = -1
  isShowDeleteDialog.value = false
}
const handleConfirmDelete = async () => {
  const { error } = await OrderApi.deleteApi(deletedRowId.value)
  if (error) {
    return
  }
  await fetchData()
  handleCloseDeleteDialog()
}
</script>
