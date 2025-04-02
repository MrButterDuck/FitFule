<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <div class="bg-white p-8 rounded-lg shadow-lg w-96">
        <h1 class="text-2xl font-bold mb-4 text-center">Вход в аккаунт</h1>
        <form @submit.prevent="login">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Логин</label>
            <input v-model="username" type="text" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md">
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Пароль</label>
            <input v-model="password" type="password" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md">
          </div>
          <button type="submit" class="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded">
            Войти
          </button>
        </form>
        <div class="mt-4 flex justify-between">
          <router-link to="/register" class="text-blue-500 hover:underline">
            Регистрация
          </router-link>
          <router-link to="/password-reset" class="text-blue-500 hover:underline">
            Забыли пароль?
          </router-link>
      </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../api';
  
  export default {
    name: 'Login',
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async login() {
        try {
          const response = await api.post('/auth/jwt/create/', {
            username: this.username,
            password: this.password,
          });
  
          localStorage.setItem('access_token', response.data.access);
          localStorage.setItem('refresh_token', response.data.refresh);
          localStorage.setItem('username', this.username);
          window.dispatchEvent(new Event('auth-changed'));
          this.$router.push('/profile');
        } catch (error) {
          const data = error.response?.data;
          const firstKey = Object.keys(data)[0];
          const firstError = data[firstKey];
          let errorMessage = 'Неверные данные'
          if (Array.isArray(firstError)) {
            errorMessage = `${firstKey}: ${firstError[0]}`;
          } else if (typeof firstError === 'string') {
            errorMessage = `${firstKey}: ${firstError}`;
          }
          this.$root.showErrorModal('Неверные логин или пароль', errorMessage);
        }
      },
    },
  };
  </script>
  