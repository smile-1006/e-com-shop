<template>
  <div>
    <h1>My Cart</h1>
    <div v-for="item in cartItems" :key="item.id">
      {{ item.product.name }} x {{ item.quantity }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const cartItems = ref([]);

onMounted(async () => {
  const res = await api.get('cart/');
  cartItems.value = res.data;
});
</script>

<script>
export default {
  name: 'UserCart'
}
</script>
