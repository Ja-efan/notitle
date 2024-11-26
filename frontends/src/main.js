import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router'; // Vue Router
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// Pinia 생성
const pinia = createPinia();

const app = createApp(App);

pinia.use(piniaPluginPersistedstate)
// Pinia와 Router 등록
app.use(pinia);
app.use(router);

// Vue 애플리케이션 마운트
app.mount('#app');
