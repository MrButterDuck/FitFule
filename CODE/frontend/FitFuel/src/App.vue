<template>
  <div class="flex flex-col min-h-screen">
    <Header />
    <router-view class="flex-grow"></router-view>
    <div>
      <ErrorModal 
        :isOpen="showError"
        :modalTitle="modalTitleText"
        :message="errorMessage"
        :isGood="isGoodModal" 
        @close="showError = false" 
      />
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import ErrorModal from "./components/ErrorModal.vue";

export default {
  name: 'App',
  components: {
    Header,
    Footer,
    ErrorModal,
  },
  data() {
    return {
      showError: false,
      errorMessage: "",
    };
  },
  methods: {
    showErrorModal(title, message, isGood) {
      this.modalTitleText = title
      this.errorMessage = message;
      this.isGoodModal = isGood
      this.showError = true;
    },
  },
  provide() {
    return {
      showErrorModal: this.showErrorModal,
    };
  },
};
</script>
