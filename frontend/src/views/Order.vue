<template>
  <div>
    <h1>Orders</h1>
    <div v-for="order in orders" :key="order.id">
      Order #{{ order.id }} - {{ order.created_at }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const orders = ref([]);

onMounted(async () => {
  const res = await api.get('orders/');
  orders.value = res.data;
});
</script>
