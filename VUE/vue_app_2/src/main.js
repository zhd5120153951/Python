import { createApp } from 'vue';
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';

const router = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/registry', component: Register },
    { path: '/hello', component: HelloWorld },
];
const route = createRouter({
    history: createWebHistory(), router,
});
