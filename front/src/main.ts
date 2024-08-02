
import '@mdi/font/css/materialdesignicons.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import "./assets/index.css"
import App from './App.vue'
import { router } from './router'
import { errorHandler } from './errorHandler'
import { BaseApi } from './api'

const pinia = createPinia()
const vuetify = createVuetify({
  components,
  directives
})
const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(vuetify)
app.config.errorHandler = (err, vm, info) => {
  errorHandler(err as BaseApi.ErrorResponseData)
}
app.mount('#app')