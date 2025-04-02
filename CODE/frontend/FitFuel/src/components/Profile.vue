<template>
  <div v-if="isAuthenticated" class="max-w-4xl mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Личный кабинет</h1>
    <div class="bg-white shadow-lg rounded-lg p-6">
      <div v-if="!isEditing" class="space-y-4">
        <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Возраст:</strong> {{ user.age || 'Не указано' }}</p>
        <p><strong>Рост:</strong> {{ user.height || 'Не указано' }} см</p>
        <p><strong>Вес:</strong> {{ user.weight || 'Не указано' }} кг</p>
        <p><strong>Аллергия:</strong></p>
        <ul v-if="user.allergyItems.length">
          <li v-for="item in user.allergyItems" :key="item.id">{{ item.name }}</li>
        </ul>
        <p v-else>Нет</p>
        <p><strong>Предпочтения:</strong></p>
        <ul v-if="user.favoriteItems.length">
          <li v-for="item in user.favoriteItems" :key="item.id">{{ item.name }}</li>
        </ul>
        <p v-else>Нет</p>
        <p><strong>Цель:</strong> {{ goals[user.goal] || 'Не указано' }}</p>
        <p><strong>Уровень активности:</strong> {{ activityLevels[user.activity_level] || 'Не указано' }}</p>
        <button @click="isEditing = true" class="bg-blue-500 text-white px-4 py-2 rounded">Редактировать</button>
      </div>

      <form v-else @submit.prevent="updateProfile" class="space-y-4">
        <input v-model="user.age" type="number" placeholder="Возраст" class="input-field">
        <input v-model="user.height" type="number" placeholder="Рост (см)" class="input-field">
        <input v-model="user.weight" type="number" placeholder="Вес (кг)" class="input-field">
        
        <div>
          <label for="allergyInput" class="block font-medium text-gray-700">Добавить аллергию:</label>
          <input
            type="text"
            v-model="allergyQuery"
            @input="searchAllergyItems"
            placeholder="Введите продукт"
            class="input-field"
            id="allergyInput"
          />
          <ul v-if="allergySuggestions.length" class="bg-white border rounded shadow-lg max-h-40 overflow-auto">
            <li
              v-for="item in allergySuggestions"
              :key="item.id"
              @click="addAllergy(item)"
              class="p-2 hover:bg-blue-100 cursor-pointer"
            >
              {{ item.name }}
            </li>
          </ul>
          <div v-if="user.allergyItems.length" class="mt-4">
            <h3 class="text-lg font-semibold mb-2">Выбранные аллергены:</h3>
            <ul class="bg-gray-100 p-2 rounded">
              <li v-for="(item, index) in user.allergyItems" :key="index" class="flex justify-between items-center">
                <span>{{ item.name }}</span>
                <button @click="removeAllergy(index)" class="text-red-500 hover:text-red-700">Удалить</button>
              </li>
            </ul>
          </div>
        </div>

        <div>
          <label for="favoriteInput" class="block font-medium text-gray-700">Добавить предпочтения:</label>
          <input
            type="text"
            v-model="favoriteQuery"
            @input="searchFavoriteItems"
            placeholder="Введите продукт"
            class="input-field"
            id="favoriteInput"
          />
          <ul v-if="favoriteSuggestions.length" class="bg-white border rounded shadow-lg max-h-40 overflow-auto">
            <li
              v-for="item in favoriteSuggestions"
              :key="item.id"
              @click="addFavorite(item)"
              class="p-2 hover:bg-blue-100 cursor-pointer"
            >
              {{ item.name }}
            </li>
          </ul>
          <div v-if="user.favoriteItems.length" class="mt-4">
            <h3 class="text-lg font-semibold mb-2">Выбранные предпочтения:</h3>
            <ul class="bg-gray-100 p-2 rounded">
              <li v-for="(item, index) in user.favoriteItems" :key="index" class="flex justify-between items-center">
                <span>{{ item.name }}</span>
                <button @click="removeFavorite(index)" class="text-red-500 hover:text-red-700">Удалить</button>
              </li>
            </ul>
          </div>
        </div>

        <select v-model="user.goal" class="input-field">
          <option value="" disabled>Выберите цель</option>
          <option value="mass_gain">Набор массы</option>
          <option value="weight_loss">Сброс веса</option>
          <option value="weight_maintenance">Поддержание веса</option>
        </select>
        <select v-model="user.activity_level" class="input-field">
          <option value="" disabled>Выберите уровень активности</option>
          <option value="low">Низкий</option>
          <option value="moderate">Умеренный</option>
          <option value="high">Высокий</option>
        </select>
        <div class="space-x-2">
          <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded">Сохранить</button>
          <button @click="isEditing = false" type="button" class="bg-gray-500 text-white px-4 py-2 rounded">Отмена</button>
        </div>
      </form>
    </div>
  </div>
  <div v-else class="inset-0 flex flex-col items-center justify-center text-center">
    <h1 class="text-3xl font-bold text-red-900 mb-4">Вы не авторизовались!</h1>
    <h2 class="text-3xl font-bold mb-4">Пожалуйста, войдите или зарегистрируйтесь</h2>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      isAuthenticated: !!localStorage.getItem('access_token'),
      user: { allergyItems: [], favoriteItems: [] },
      isEditing: false,
      allergyQuery: '',
      allergySuggestions: [],
      favoriteQuery: '',
      favoriteSuggestions: [],
      goals: {
        mass_gain: 'Набор массы',
        weight_loss: 'Сброс веса',
        weight_maintenance: 'Поддержание веса'
      },
      activityLevels: {
        low: 'Низкий',
        moderate: 'Умеренный',
        high: 'Высокий'
      }
    };
  },
  mounted() {
    this.fetchUser();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await api.get('/auth/users/me/');
        this.user = { ...response.data, allergyItems: [], favoriteItems: [] };
        if (this.user.allergy.length > 0) {
          const allergyResponse = await api.get(`/products/?ids=${this.user.allergy.join(',')}`);
          this.user.allergyItems = allergyResponse.data;
        } else {
          this.user.allergyItems = [];
        }

        if (this.user.favorites.length > 0) {
          const favoriteResponse = await api.get(`/products/?ids=${this.user.favorites.join(',')}`);
          this.user.favoriteItems = favoriteResponse.data;
        } else {
          this.user.favoriteItems = [];
        }
      } catch (error) {
        console.error('Ошибка при получении данных пользователя:', error);
      }
    },
    async updateProfile() {
      try {
        // Собираем ID только из массива allergyItems
        const allergyIds = this.user.allergyItems.map(item => item.id);
        const favoriteIds = this.user.favoriteItems.map(item => item.id);

        // Отправляем данные с корректным форматом
        const updatedData = { 
          ...this.user, 
          allergy: allergyIds,
          favorites: favoriteIds
        };

        // Отправляем запрос на сервер
        await api.put('/auth/users/me/', updatedData);

        // Обновляем интерфейс после успешного сохранения
        this.isEditing = false;
        this.fetchUser(); // Повторный запрос для обновления данных
      } catch (error) {
        console.error('Ошибка при обновлении профиля:', error);
      }
    },
    async searchAllergyItems() {
      if (this.allergyQuery.length < 2) {
        this.allergySuggestions = [];
        return;
      }
      try {
        const response = await api.get(`/products/?search=${this.allergyQuery}`);
        this.allergySuggestions = response.data.filter(item =>
          item.name.toLowerCase().includes(this.allergyQuery.toLowerCase())
        );
      } catch (error) {
        console.error('Ошибка при поиске аллергенов:', error);
      }
    },
    addAllergy(item) {
      if (!this.user.allergyItems.some(allergy => allergy.id === item.id)) {
        this.user.allergyItems.push(item);
      }
      this.allergyQuery = '';
      this.allergySuggestions = [];
    },
    removeAllergy(index) {
      this.user.allergyItems.splice(index, 1);
    },
    async searchFavoriteItems() {
      if (this.favoriteQuery.length < 2) {
        this.favoriteSuggestions = [];
        return;
      }
      try {
        const response = await api.get(`/products/?search=${this.favoriteQuery}`);
        this.favoriteSuggestions = response.data.filter(item =>
          item.name.toLowerCase().includes(this.favoriteQuery.toLowerCase())
        );
      } catch (error) {
        console.error('Ошибка при поиске предпочтений:', error);
      }
    },
    addFavorite(item) {
      if (!this.user.favoriteItems.some(favorites => favorites.id === item.id)) {
        this.user.favoriteItems.push(item);
      }
      this.favoriteQuery = '';
      this.favoriteSuggestions = [];
    },
    removeFavorite(index) {
      this.user.favoriteItems.splice(index, 1);
    }
  }
};
</script>

<style>
.input-field {
  @apply block w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300;
}
</style>
