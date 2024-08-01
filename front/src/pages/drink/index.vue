<template>
  <v-container style="display: flex;justify-content: center;">
    <v-data-table density="compact" style="max-width: fit-content;text-align: center;" hide-default-footer
      :headers="headers" :items="drinkDataList">
      <template v-slot:top>
        <v-btn class="mb-2 ml-auto" color="primary" dark @click="handleClickCreate">
          新增飲品
        </v-btn>
        <v-dialog v-model="isShowDialog" max-width="500px">
          <v-form v-model="isFormValid" validate-on="input" @submit.prevent>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ dialogTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-text-field v-model="editedData.name" validate-on="input" :rules="[inputRules.requiredString]"
                    label="名稱" />
                  <v-text-field v-model="editedData.price" validate-on="input" :rules="[inputRules.requiredPositiveInt]"
                    label="價格" />
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn color="blue-darken-1" variant="text" @click="handleCloseDialog">
                  取消
                </v-btn>
                <v-btn color="blue-darken-1" type="submit" variant="text" @click="handleDialogSubmit">
                  送出
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-form>
        </v-dialog>
        <v-dialog v-model="isShowDeleteDialog" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">確定要刪除{{ deletedRowName }}嗎?</v-card-title>
            <v-card-actions>
              <v-spacer />
              <v-btn color="blue-darken-1" variant="text" @click="handleCloseDeleteDialog">取消</v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="handleConfirmDelete">刪除</v-btn>
              <v-spacer />
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon class="me-2" size="small" @click="handleClickEdit(item)">
          mdi-pencil
        </v-icon>
        <v-icon size="small" @click="handleClickDelete(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
import { DrinkApi } from '../../api';
import { inputRules } from '../../utils';
const headers = [
  {
    title: '序號',
    key: 'id',
    sortable: false
  },
  {
    title: '名稱',
    key: 'name',
    sortable: false
  },
  {
    title: '價格',
    key: 'price',
    sortable: false
  },
  {
    title: '編輯、刪除',
    key: 'actions',
    sortable: false
  },
]
const drinkDataList = ref<DrinkApi.GetResponse[]>([])
const fetchData = async () => {
  const { response } = await DrinkApi.CRUD.getAllApi()
  if (response) {
    drinkDataList.value = response
  }
}

//delete dialog
const deletedRowName = ref("")
const deletedRowId = ref(-1)
const isShowDeleteDialog = ref(false)
const handleClickDelete = (row: DrinkApi.GetResponse) => {
  deletedRowName.value = row.name
  deletedRowId.value = row.id
  isShowDeleteDialog.value = true
}
const handleConfirmDelete = async () => {
  const { error } = await DrinkApi.CRUD.deleteApi(deletedRowId.value)
  if (error) {
    return
  }
  await fetchData()
  handleCloseDeleteDialog()
}
const handleCloseDeleteDialog = () => {
  isShowDeleteDialog.value = false
}

//dialog
const isFormValid = ref(false)
const isShowDialog = ref(false)
const editedDataId = ref(-1)
const dialogTitle = computed(() => {
  return editedDataId.value === -1 ? '新增飲品' : '編輯飲品'
})
const isCreate = () => editedDataId.value === -1
const editedData = ref<DrinkApi.UpdateData>({
  name: '',
  price: 0
})
const defaultData = {
  name: '',
  price: 0
}
const handleClickEdit = (row: DrinkApi.GetResponse) => {
  editedDataId.value = row.id
  editedData.value = Object.assign({}, row)
  isShowDialog.value = true
}
const handleClickCreate = () => {
  editedDataId.value = -1
  editedData.value = Object.assign({}, defaultData)
  isShowDialog.value = true
}
const handleCloseDialog = () => {
  isShowDialog.value = false
}
const handleDialogSubmit = async () => {
  if (!isFormValid.value) {
    return
  }
  let error: any
  if (isCreate()) {
    const res = await DrinkApi.CRUD.createApi(editedData.value)
    error = res.error
  } else {
    const res = await DrinkApi.CRUD.updateApi(editedDataId.value, editedData.value)
    error = res.error
  }
  if (error) {
    return
  }
  await fetchData()
  handleCloseDialog()
}
onBeforeMount(() => {
  fetchData()
})
</script>
