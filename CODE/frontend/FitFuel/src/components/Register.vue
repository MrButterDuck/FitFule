<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <div class="bg-white p-8 rounded-lg shadow-lg w-96">
        <h1 class="text-2xl font-bold mb-4 text-center">Регистрация</h1>
        <form @submit.prevent="register">
          <!-- Логин -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Логин</label>
            <input v-model="username" type="text" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>
  
          <!-- Email -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input v-model="email" type="email" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>
  
          <!-- Пароль -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Пароль</label>
            <input v-model="password" type="password" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>
  
          <!-- Подтверждение пароля -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Подтвердите пароль</label>
            <input v-model="passwordConfirm" type="password" required class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>
  
          <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Зарегистрироваться
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import api from '../api';
  
  export default {
    name: 'Register',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        passwordConfirm: '',
      };
    },
    methods: {
      async register() {
        if (this.password !== this.passwordConfirm) {
          alert('Пароли не совпадают!');
          return;
        }
        try {
          await api.post('/auth/users/', {
            username: this.username,
            email: this.email,
            password: this.password,
          });
          alert('Регистрация прошла успешно! Теперь войдите в аккаунт.');
          this.$router.push('/login');
        } catch (error) {
          alert('Ошибка при регистрации: ' + (error.response?.data?.detail || 'Попробуйте снова.'));
        }
      },
    },
  };
  </script>
  