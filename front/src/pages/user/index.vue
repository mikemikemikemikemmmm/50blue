<template>
  <v-container style="display: flex;justify-content: center;">
    <v-data-table density="compact" style="max-width: fit-content;text-align: center;" hide-default-footer
      :headers="headers" :items="dataList">
      <template v-slot:top>
        <v-btn class="mb-2 ml-auto" color="primary" dark @click="handleClickCreate">
          新增用戶
        </v-btn>
        <v-dialog v-model="isShowDialog" max-width="500px">
          <v-form v-model="isFormValid" validate-on="input" @submit.prevent>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ dialogTitle }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-text-field v-model="editedData.email" validate-on="input" :rules="[inputRules.requiredString]"
                    label="信箱" />
                  <v-text-field type="password" v-model="editedData.password" validate-on="input"
                    :rules="[inputRules.requiredString]" label="密碼" />
                  <v-text-field type="password" v-model="editedData.password2" validate-on="input"
                    :rules="[inputRules.requiredString]" label="請再輸入一次密碼" />
                  <v-select v-model="editedData.role" label="角色" :items="USER_ROLE_LIST" />
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
        <!-- <v-icon class="me-2" size="small" @click="handleClickEdit(item)">
          mdi-pencil
        </v-icon> -->
        <v-icon size="small" @click="handleClickDelete(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
import {  UserApi } from '../../api';
import { inputRules } from '../../utils';
import { USER_ROLE, USER_ROLE_LIST } from '../../const';
import { useGlobalStore } from '../../store';
const headers = [
  {
    title: '信箱',
    key: 'email',
    sortable: false
  },
  {
    title: '角色',
    key: 'role_str',
    sortable: false
  },
  {
    title: '刪除',
    key: 'actions',
    sortable: false
  },
]
const dataList = ref<UserApi.GetResponse[]>([])
const fetchData = async () => {
  const { response } = await UserApi.CRUD.getAllApi()
  if (response) {
    dataList.value = response
  }
}

//delete dialog
const deletedRowName = ref("")
const deletedRowId = ref(-1)
const isShowDeleteDialog = ref(false)
const handleClickDelete = (row: UserApi.GetResponse) => {
  deletedRowName.value = row.email
  deletedRowId.value = row.id
  isShowDeleteDialog.value = true
}
const handleConfirmDelete = async () => {
  const { error } = await UserApi.CRUD.deleteApi(deletedRowId.value)
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
  return editedDataId.value === -1 ? '新增用戶' : '編輯用戶'
})
const isCreate = () => editedDataId.value === -1
const editedData = ref<UserApi.CreateData>({
  email: '',
  password: "",
  password2: "",
  role: USER_ROLE.CLERK
})
const defaultData = {
  email: '',
  password: "",
  password2: "",
  role: USER_ROLE.CLERK
}
// const handleClickEdit = (row: DrinkApi.GetResponse) => {
//   editedDataId.value = row.id
//   editedData.value = Object.assign({}, row)
//   isShowDialog.value = true
// }
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
  if (editedData.value.password !== editedData.value.password2) {
    const store = useGlobalStore()
    store.createAlertData({ type: "error", text: "兩次密碼不同" })
    return
  }
  if (isCreate()) {
    const { error } = await UserApi.CRUD.createApi(editedData.value)
    if (error) {
      return
    }
    await fetchData()
    handleCloseDialog()
  }
}
onBeforeMount(() => {
  fetchData()
})
</script>
