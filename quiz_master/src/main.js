import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)

app.use(store)
app.use(router)


// Initialize auth on app start
store.dispatch('loadAuthFromStorage')

app.mount('#app')
