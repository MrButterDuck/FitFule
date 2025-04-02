<template class="bg-beige">
    <div class="max-w-4xl mx-auto p-4">
      <h1 class="text-3xl font-bold mb-6">Подбор меню</h1>
        <div class="bg-white shadow rounded-lg p-6 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Цена (мин - макс)</label>
                    <div class="flex space-x-2 mt-2">
                        <input v-model="filters.priceMin" type="number" min="0"placeholder="Мин" class="w-full p-2 border rounded">
                        <input v-model="filters.priceMax" type="number" min="0" placeholder="Макс" class="w-full p-2 border rounded">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Калории</label>
                    <Slider v-model="calorieRange" :min="0" :max="1000" :tooltip="true" class="mt-2" />
                    <div class="flex justify-between text-sm text-gray-600 mt-2">
                        <span>{{ calorieRange[0] }} ккал</span>
                        <span>{{ calorieRange[1] }} ккал</span>
                    </div>
                </div>
                <div :class="{ 'col-span-2': !isAuthenticated, 'col-span-1': isAuthenticated }">
                <label class="block text-sm font-medium text-gray-700">Время приема пищи</label>
                <select v-model="filters.mealTime" class="w-full p-2 border rounded mt-2">
                    <option value="">Любое</option>
                    <option value="breakfast">Завтрак</option>
                    <option value="lunch">Обед</option>
                    <option value="dinner">Ужин</option>
                    <option value="snack">Перекус</option>
                </select>
                </div>
                <div v-if="isAuthenticated" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="flex items-center md:justify-end mt-4 md:mt-0">
                        <input type="checkbox" id="excludeAllergens" v-model="filters.excludeAllergens" class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                        <label for="excludeAllergens" class="ml-2 text-sm text-gray-700">Исключить аллергены</label>
                    </div>
                    <div class="flex items-center">
                        <input type="checkbox" id="includeFavorites" v-model="filters.includeFavorites" class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                        <label for="includeFavorites" class="ml-2 text-sm text-gray-700">Учитывать предпочтения</label>
                    </div>
                </div>
            </div>
                <div class="mt-6">
                    <label for="favoriteInput" class="block text-sm font-medium text-gray-700">Добавить предпочтения:</label>
                    <input
                        type="text"
                        v-model="favoriteQuery"
                        @input="searchFavoriteItems"
                        placeholder="Введите продукт"
                        class="w-full border rounded p-2 mt-2"
                        id="favoriteInput"
                    />
                    <ul v-if="favoriteSuggestions.length" class="bg-white border rounded shadow-lg max-h-40 overflow-auto mt-2">
                        <li
                        v-for="item in favoriteSuggestions"
                        :key="item.id"
                        @click="addFavorite(item)"
                        class="p-2 hover:bg-blue-100 cursor-pointer"
                        >
                        {{ item.name }}
                        </li>
                    </ul>
                    <div v-if="filters.includeProducts.length" class="mt-4">
                        <h3 class="text-lg font-semibold mb-2">Выбранные предпочтения:</h3>
                        <ul class="bg-gray-100 p-2 rounded">
                        <li v-for="(item, index) in filters.includeProducts" :key="index" class="flex justify-between items-center">
                            <span>{{ item.name }}</span>
                            <button @click="removeFavorite(index)" class="text-red-500 hover:text-red-700">Удалить</button>
                        </li>
                        </ul>
                    </div>
                 </div>
        
            <!-- Кнопка применения фильтров -->
            <button @click="applyFilters" class="mt-6 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                Применить фильтр
            </button>
        </div>
 
  
      <!-- Список блюд -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="dish in dishes" :key="dish.id" class="bg-white shadow rounded-lg p-4">
        <h2 class="text-xl font-bold">{{ dish.name }}</h2>
        <p class="text-sm text-gray-600">Цена: {{ dish.price }} ₽</p>
        <p class="text-sm text-gray-600">Калории: {{ (dish.calories).toFixed(3) }} ккал</p>
        <p class="text-sm text-gray-600">Тип: {{ mealTypeLabel(dish.meal_type) }}</p>
        <button @click="toggleIngredients(dish.id)" class="mt-2 text-blue-500 hover:underline">
          {{ showIngredients[dish.id] ? 'Скрыть ингредиенты' : 'Показать ингредиенты' }}
        </button>
        <ul v-if="showIngredients[dish.id]" class="mt-2 bg-gray-100 p-2 rounded">
          <li v-for="ingredient in dish.recipe_ingredients" :key="ingredient.id">{{ ingredient.product.name }}</li>
        </ul>
      </div>
    </div>
    <div v-if="loading" class="text-center mt-4">Загрузка...</div>
    <div v-if="!loading && !hasMore" class="text-center mt-4 text-gray-500">Карточек больше нет</div>
    <button v-if="hasMore && !loading" @click="loadMore" class="mt-6 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 w-full">Загрузить ещё</button>
    </div>
  </template>
  
  <script>
  import api from '../api';
  import '@vueform/slider/themes/default.css'
  import Slider from '@vueform/slider'
  
  export default {
    components: { Slider },
    data() {
      return {
        isAuthenticated: !!localStorage.getItem('access_token'),
        filters: {
          priceMin: '',
          priceMax: '',
          mealTime: '',
          excludeAllergens: false,
          includeFavorites: false,
          includeProducts: [],
        },
        calorieRange: [0, 1000],
        dishes: [],
        favoriteQuery: '',
        favoriteSuggestions: [],
        showIngredients: {},
        page: 1,
        pageSize: 9,
        loading: false,
        hasMore: true,
      };
    },
    methods: {
        async fetchDishes(reset = false) {
            if (reset) {
                this.page = 1;
                this.dishes = [];
                this.hasMore = true;
            }
            if (this.filters.priceMin < 0 || this.filters.priceMax < 0 || this.filters.priceMin > this.filters.priceMax){
                this.$root.showErrorModal('Некорректный ввод', 'проверьте поля ввода цены');
                return;
            }
            if (this.loading || !this.hasMore) return;
                this.loading = true;
            const params = {
                price_min: this.filters.priceMin || undefined,
                price_max: this.filters.priceMax || undefined,
                calories: `${this.calorieRange[0]}-${this.calorieRange[1]}`,
                meal_type: this.filters.mealTime || undefined,
                exclude_allergens: this.filters.excludeAllergens || undefined,
                include_favorites: this.filters.includeFavorites || undefined,
                include_products: this.filters.includeProducts.map(p => p.id).join(',') || undefined,
                limit: this.pageSize,
                offset: (this.page - 1) * this.pageSize,
            };

            try {
                const response = await api.get('/recipes/', { params });
                this.hasMore = response.data.next !== null
                this.dishes = reset ? response.data.results : [...this.dishes, ...response.data.results];
                this.page++;
            } catch (error) {
                console.error('Ошибка при загрузке блюд:', error);
            } finally {
                this.loading = false;
            }
        },
        async applyFilters() {
            await this.fetchDishes(true);
        },
        loadMore() {
            this.fetchDishes();
        },
        mealTypeLabel(type) {
            const labels = {
            breakfast: 'Завтрак',
            lunch: 'Обед',
            dinner: 'Ужин',
            snack: 'Перекус',
            };
            return labels[type] || 'Неизвестно';
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
        if (!this.filters.includeProducts.some(favorite => favorite.id === item.id)) {
            this.filters.includeProducts.push(item);
        }
        this.favoriteQuery = '';
        this.favoriteSuggestions = [];
        },
        removeFavorite(index) {
        this.filters.includeProducts.splice(index, 1);
        },
        toggleIngredients(dishId) {
            this.showIngredients[dishId] = !this.showIngredients[dishId];
        },
    },
    mounted() {
      this.applyFilters();
    },
  };
  </script>
  
  <style>
  body {
    font-family: 'Arial', sans-serif;
    background: #f3f4f6;
  }
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
  