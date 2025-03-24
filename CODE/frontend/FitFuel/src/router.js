import { createRouter, createWebHistory } from 'vue-router';
import Register from './components/Register.vue';
import Login from './components/Login.vue';
import Home from './components/Home.vue';
import Profile from './components/Profile.vue';
import Menu from './components/Menu.vue';
import ResetPassword from './components/ResetPassword.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/profile',  component: Profile },
  { path: '/menu',  component: Menu },
  { path: '/password-reset',  component: ResetPassword },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
