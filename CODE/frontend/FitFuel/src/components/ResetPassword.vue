<template>
    <div class="flex items-center justify-center h-screen bg-gray-100">
      <div class="w-full max-w-md p-8 bg-white rounded shadow-md">
        <h2 class="text-2xl font-bold mb-6 text-center">Сброс пароля</h2>
        <form @submit.prevent="handlePasswordUpdate">
          <div class="mb-4">
            <label for="new-password" class="block mb-2 text-sm font-medium">Новый пароль</label>
            <input
              v-model="newPassword"
              id="new-password"
              type="password"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Введите новый пароль"
              required
            />
          </div>
          <div class="mb-4">
            <label for="confirm-password" class="block mb-2 text-sm font-medium">Подтверждение пароля</label>
            <input
              v-model="confirmPassword"
              id="confirm-password"
              type="password"
              class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Подтвердите новый пароль"
              required
            />
          </div>
          <button
            type="submit"
            class="w-full py-2 px-4 bg-blue-500 text-white font-bold rounded hover:bg-blue-600"
          >
            Сохранить новый пароль
          </button>
        </form>
        <p v-if="message" class="mt-4 text-green-500">{{ message }}</p>
        <p v-if="error" class="mt-4 text-red-500">{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import api from "../api"; // Подключение вашего API-файла
  
  export default {
    data() {
      return {
        newPassword: "",
        confirmPassword: "",
        message: "",
        error: "",
      };
    },
    methods: {
      async handlePasswordUpdate() {
        if (this.newPassword !== this.confirmPassword) {
          this.error = "Пароли не совпадают.";
          this.message = "";
          return;
        }
  
        try {
          const token = this.$route.query.token;
          await api.post("/password/reset/confirm/", {
            token: token,
            new_password: this.newPassword,
          });
          this.message = "Пароль успешно обновлён.";
          this.error = "";
        } catch (err) {
          this.error = "Ошибка при обновлении пароля.";
          this.message = "";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Добавьте стили, если необходимо */
  </style>
  