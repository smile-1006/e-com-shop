<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld :msg="message"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    HelloWorld
  },
  data() {
    return {
      message: ''
    }
  },
  mounted() {
    axios.get('/api/date')
      .then(response => {
        this.message = `Welcome to Your Vue.js App. Current date is: ${response.data.date}`
      })
      .catch(error => {
        console.error(error)
      })
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
