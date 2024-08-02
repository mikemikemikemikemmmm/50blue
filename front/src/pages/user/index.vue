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
                  <v-text-field v-if="editingType === 'create_new_user'" v-model="editedData.email" validate-on="input"
                    :rules="[inputRules.requiredString]" label="信箱" />
                  <v-text-field v-if="editingType !== 'edit_role'" type="password" v-model="editedData.password"
                    validate-on="input" :rules="[inputRules.requiredString]" label="密碼" />
                  <v-text-field v-if="editingType !== 'edit_role'" type="password" v-model="editedData.password2"
                    validate-on="input" :rules="[inputRules.requiredString]" label="請再輸入一次密碼" />
                  <v-select v-if="editingType !== 'edit_password'" v-model="editedData.role" label="角色"
                    :items="USER_ROLE_LIST" />
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
        <v-icon class="me-2" size="small" @click="handleClickEdit(item, 'edit_password')">
          mdi-key-variant
        </v-icon>
        <v-icon class="me-2" size="small" @click="handleClickEdit(item, 'edit_role')">
          mdi-human-male
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
import { UserApi } from '../../api';
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
    title: '修改密碼、修改角色、刪除',
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
type EditType = "edit_password" | "edit_role" | "create_new_user"
const editingType = ref<EditType>("edit_password")
const isFormValid = ref(false)
const isShowDialog = ref(false)
interface EditingData extends UserApi.CreateData {
  id: number,
  password2: string
}
const editedData = ref<EditingData>({
  id: -1,
  email: '',
  password: "",
  password2: "",
  role: USER_ROLE.CLERK
})
const defaultDataForCreate = {
  id: -1,
  email: '',
  password: "",
  password2: "",
  role: USER_ROLE.CLERK
}
const dialogTitle = computed(() => {
  return editedData.value.id === -1 ? `新增用戶` : `編輯${editedData.value.email}`
})
const handleClickEdit = (row: UserApi.GetResponse, _editingType: EditType) => {
  editingType.value = _editingType
  editedData.value = {
    id: row.id,
    email: row.email,
    password: "",
    password2: "",
    role: row.role_str
  }
  isShowDialog.value = true
}
const handleClickCreate = () => {
  editingType.value = "create_new_user"
  editedData.value = Object.assign({}, defaultDataForCreate)
  isShowDialog.value = true
}
const handleCloseDialog = () => {
  isShowDialog.value = false
}
const handleDialogSubmit = async () => {
  if (!isFormValid.value) {
    return
  }
  if (
    editingType.value !== "edit_role" &&
    (editedData.value.password !== editedData.value.password2)
  ) {
    const store = useGlobalStore()
    store.createAlertData({ type: "error", text: "兩次密碼不同" })
    return
  }
  const targetApi = (() => {
    if (editingType.value === 'create_new_user') {
      return UserApi.CRUD.createApi(editedData.value)
    } else if (editingType.value === 'edit_password') {
      return UserApi.updatePasswordApi(editedData.value.id, editedData.value.password)
    } else {
      return UserApi.updateRoleApi(editedData.value.id, editedData.value.role)
    }
  })()
  const { error } = await targetApi
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
