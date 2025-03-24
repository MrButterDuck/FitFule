<template>
    <header class="bg-olive p-4 flex justify-between items-center">
      <div class="flex items-center">
        <!-- Логотип -->
        <a href="/" class="text-white font-bold text-2xl mr-8">FitFuel</a>
        <!-- Навигация -->
        <nav>
          <a href="/" class="text-white mr-4 hover:underline">Главная</a>
          <a href="/menu" class="text-white mr-4 hover:underline">Подбор меню</a>
          <a href="/profile" class="text-white hover:underline">Личный кабинет</a>
        </nav>
      </div>
  
      <!-- Кнопка входа/выхода -->
      <div>
        <template v-if="isAuthenticated">
          <span class="text-white mr-4">Привет, {{ username }}!</span>
          <button @click="logout" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
            Выйти
          </button>
        </template>
        <template v-else>
          <button @click="goToLogin" class="bg-green-500 hover:bg-beige text-white font-bold py-2 px-4 rounded">
            Вход
          </button>
        </template>
      </div>
    </header>
  </template>
  
  <script>
  export default {
    name: 'Header',
    data() {
      return {
        isAuthenticated: !!localStorage.getItem('access_token'),
        username: localStorage.getItem('username') || 'Пользователь',
      };
    },
    mounted() {
      // Ловим событие обновления аутентификации
      window.addEventListener('auth-changed', this.updateUser);
    },
    beforeDestroy() {
      window.removeEventListener('auth-changed', this.updateUser);
    },
    methods: {
      goToLogin() {
        this.$router.push('/login');
      },
      logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
        this.updateUser();
        this.$router.push('/login');
      },
      updateUser() {
        this.isAuthenticated = !!localStorage.getItem('access_token');
        this.username = localStorage.getItem('username') || 'Пользователь';
      },
    },
  };
  </script>

<style>
.bg-beige {
  background-color: #f5f5dc;
}
.text-olive {
  color: #556b2f;
}
.bg-olive {
  background-color: #556b2f;
}
.bg-olive-dark {
  background-color: #6b8e23;
}
.bg-olive-light {
  background-color: #dcdcb4;
}
</style>