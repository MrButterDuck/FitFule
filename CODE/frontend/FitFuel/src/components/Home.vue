<template>
    <div class="flex flex-col min-h-screen">
      <main class="flex-grow container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-6">Калькулятор калорий</h1>
  
        <form @submit.prevent="calculateCalories" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div class="mb-4">
            <label class="block text-sm font-bold mb-2" for="product">
              Название продукта/блюда:
            </label>
            <input
              type="text"
              v-model="searchQuery"
              @input="searchItems"
              placeholder="Введите название продукта или блюда"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
  
            <ul v-if="suggestions.length" class="bg-white border rounded shadow-lg max-h-40 overflow-auto">
              <li
                v-for="item in suggestions"
                :key="item.id"
                @click="addItem(item)"
                class="p-2 hover: cursor-pointer"
              >
                {{ item.name }}
              </li>
            </ul>
          </div>
  
          <div v-if="selectedItems.length" class="mb-4">
            <h3 class="text-lg font-semibold mb-2">Выбранные продукты/блюда:</h3>
            <ul class=" p-2 rounded">
              <li v-for="(item, index) in selectedItems" :key="index" class="flex justify-between items-center p-2 border-b">
                <div class="flex items-center space-x-2">
                  <span>{{ item.name }}</span>
                  <input
                    type="number"
                    v-model.number="item.quantity"
                    min="1"
                    class="w-16 px-2 py-1 border rounded"
                  />
                  <span>{{ Math.max((item.calories * item.quantity).toFixed(3), 0) }} ккал</span>
                </div>
                <button @click="removeItem(index)" class="text-red-500 hover:text-red-700">Удалить</button>
              </li>
            </ul>
          </div>
  
          <button
            type="submit"
            class="w-full bg-olive hover:bg-olive-dark text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Рассчитать калорийность
          </button>
        </form>
  
        <div v-if="result" class="bg-white p-4 rounded shadow-md">
          <h2 class="text-2xl font-bold mb-2">Итоговая калорийность:</h2>
          <div class="flex items-center justify-center mb-4">
            <PieChart :chart-data="chartData" :chart-options="chartOptions" />
          </div>
          <p>Калории: {{ result.calories }} ккал</p>
          <p>Белки: {{ result.proteins }} г</p>
          <p>Жиры: {{ result.fats }} г</p>
          <p>Углеводы: {{ result.carbs }} г</p>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import api from '../api';
  import { PieChart } from 'vue-chart-3';
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);
  
  export default {
    name: 'Home',
    components: { PieChart },
    data() {
      return {
        searchQuery: '',
        suggestions: [],
        selectedItems: [],
        result: null,
      };
    },
    computed: {
      chartData() {
        if (!this.result) return {};
        return {
          labels: ['Белки', 'Жиры', 'Углеводы'],
          datasets: [
            {
              backgroundColor: ['#556B2F', '#8B4513', '#F5DEB3'],
              data: [this.result.proteins, this.result.fats, this.result.carbs],
            },
          ],
        };
      },
      chartOptions() {
        return {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
            },
          },
        };
      },
    },
    methods: {
      async searchItems() {
        if (this.searchQuery.length < 2) {
          this.suggestions = [];
          return;
        }
        try {
          const [productsResponse, recipesResponse] = await Promise.all([
            api.get(`/products/?search=${this.searchQuery}`),
            api.get(`/recipes/?search=${this.searchQuery}`),
          ]);
          const query = this.searchQuery.toLowerCase();
          this.suggestions = [
            ...productsResponse.data.filter((item) => item.name.toLowerCase().includes(query)),
            ...recipesResponse.data.results.filter((item) => item.name.toLowerCase().includes(query)),
          ];
        } catch (error) {
          console.error('Ошибка при поиске:', error);
        }
      },
      addItem(item) {
        const selectedItem = { ...item, quantity: 1 };
        this.selectedItems.push(selectedItem);
        this.searchQuery = '';
        this.suggestions = [];
      },
      removeItem(index) {
        this.selectedItems.splice(index, 1);
      },
      calculateCalories() {
        const total = this.selectedItems.reduce(
          (acc, item) => {
            acc.calories += +(item.calories * item.quantity).toFixed(3);
            acc.proteins += +(item.proteins * item.quantity).toFixed(3);
            acc.fats += +(item.fats * item.quantity).toFixed(3);
            acc.carbs += +(item.carbohydrates * item.quantity).toFixed(3);
            return acc;
          },
          { calories: 0, proteins: 0, fats: 0, carbs: 0 }
        );
        this.result = total;
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
  