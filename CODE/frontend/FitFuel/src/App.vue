<template>
  <div class="flex flex-col min-h-screen">
    <Header />
    <router-view class="flex-grow"></router-view>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    Header,
    Footer,
  },
};
</script>
