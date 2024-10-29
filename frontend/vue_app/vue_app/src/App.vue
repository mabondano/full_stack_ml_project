<template>
  <div id="app">
    <h1>Full Stack ML Project</h1>
    <SignalInput />
  </div>
</template>

<script>
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

