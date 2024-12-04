import { createApp } from 'vue';
import App from './App.vue';
// import axiosInstance from './axios';
import store from './configuration/vuex';
import routers from './configuration/routers';
import mixins from './configuration/mixins';

import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-default.css'

const app = createApp(App);

// Globally add Axios to the app
// app.config.globalProperties.$axios = axiosInstance;

app.use(store);
app.use(routers);
app.use(VueToast,{
    queue:false,
    position: 'bottom-right',
    duration: 5000,
    dismissible: true,
    closeOnClick: true,
    pauseOnHover: true,
})

app.mixin(mixins);
app.mount('#app');

