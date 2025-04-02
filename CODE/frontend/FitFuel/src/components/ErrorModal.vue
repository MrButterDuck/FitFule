<template>
    <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-180">
        <h2 v-if="isGood" class="text-xl font-semibold text-green-600">{{ modalTitle }}</h2>
        <h2 v-else class="text-xl font-semibold text-red-600">{{ modalTitle }}</h2>
        <p class="mt-2">{{ message }}</p>
        <div class="mt-4 flex justify-end">
          <button v-if="isGood" @click="closeModal" class="px-4 py-2 bg-green-500 text-white rounded">Ок</button>
          <button v-else @click="closeModal" class="px-4 py-2 bg-red-500 text-white rounded">Закрыть</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      isOpen: {
        type: Boolean,
        required: true,
      },
      isGood: {
        type: Boolean,
        default: false,
      },
      modalTitle: {
        type: String,
        default: "Ошибка",
      },
      message: {
        type: String,
        default: "Произошла ошибка",
      },
    },
    methods: {
      closeModal() {
        this.$emit("close");
      },
    },
  };
  </script>
  

  