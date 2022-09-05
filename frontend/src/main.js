import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import MainPage from "./views/MainPage.vue";
import ScenarioPage from "./views/ScenarioPage.vue";
import AboutPage from "./views/AboutPage.vue";

const app = createApp(App);

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', component: MainPage},
        {path: '/scenarios', component: ScenarioPage},
        {path: '/about', component: AboutPage},
    ]
});

app.use(router);

app.mount('#app');
