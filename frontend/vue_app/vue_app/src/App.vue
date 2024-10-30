<template>
  <div id="app">
    <h1>Full Stack ML Project</h1>
    <SignalInput />
  </div>
</template>

<script>
// En main.js o App.vue
import './assets/styles.css'; // Asegúrate de usar la ruta correcta según donde lo guardaste

import SignalInput from './components/SignalInput.vue';

export default {
  name: 'App',
  components: {
    SignalInput
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 40px;
}
</style>

