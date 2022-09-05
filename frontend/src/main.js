import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import MainPage from "./components/pages/MainPage.vue";
import ScenarioPage from "./components/pages/ScenarioPage.vue";
import AboutPage from "./components/pages/AboutPage.vue";

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
