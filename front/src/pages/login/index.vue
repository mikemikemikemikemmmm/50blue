<script setup lang="ts">
import { ref } from 'vue';
import { loginApi } from '../../api/auth';
import { inputRules, setToken } from '../../utils';
import { useGlobalStore } from '../../store';
import { useRouter } from 'vue-router';
const router = useRouter()
const store = useGlobalStore()

const pasword = ref("")
const email = ref("")

const handleSubmit = async () => {
  const { response,error } = await loginApi(email.value, pasword.value)
  if (error) {
    return
  }
  setToken(response.access_token)
  store.setAllowRouteNameList(response.allow_route_name_list)
  router.push({ name: response.allow_route_name_list[0] })
}
</script>

<template>
  <div class="all-item-center">
    <v-sheet width="200">
      <v-form fast-fail @submit.prevent>
        <v-text-field v-model="email" :rules="[inputRules.requiredString]" label="信箱"></v-text-field>
        <v-text-field type="password" v-model="pasword" :rules="[inputRules.requiredString]" label="密碼"></v-text-field>
        <v-btn class="mt-2" type="submit" @click="handleSubmit" block>登入</v-btn>
      </v-form>
    </v-sheet>
  </div>
</template>
