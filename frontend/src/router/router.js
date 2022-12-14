/* eslint-disable */
import { createRouter, createWebHistory } from 'vue-router';

import auth from '../cognito/auth';

import MainPage from "../components/pages/MainPage.vue";
import ScenarioPage from "../components/pages/ScenarioPage.vue";
import AboutPage from "../components/pages/AboutPage.vue";
import LogoutSuccess from "../components/pages/LogoutSuccess.vue";
import ErrorPage from "../components/pages/ErrorPage.vue";


function requireAuth(to, from, next) {

    if (!auth.auth.isUserSignedIn()) {
        next({
            path: '/login',
            query: { redirect: to.fullPath }
        });
    } else {
        next();
    };
}

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: MainPage,
            beforeEnter: requireAuth
        },
        {
            path: '/login', beforeEnter(to, from, next) {
                auth.login();
            }
        },

        {
            path: '/login/oauth2/code/cognito', beforeEnter(to, from, next) {
                var currUrl = window.location.href;
                auth.auth.parseCognitoWebResponse(currUrl);
            }
        },

        {
            path: '/logout', component: LogoutSuccess, beforeEnter(to, from, next) {
                auth.logout();
                next();
            }

        },

        {
            path: '/error', component: ErrorPage
        },

        {
            path: '/scenarios',
            component: ScenarioPage,
            beforeEnter: requireAuth
        },

        {
            path: '/about',
            component: AboutPage
        },
    ]
});
