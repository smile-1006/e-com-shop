<template>
  <div class="product-list">
    <h2>Available Products</h2>
    <ul>
      <li v-for="product in products" :key="product.id" class="product-item">
        <router-link :to="{ name: 'ProductDetail', params: { name: product.product_name } }">
          <h3>{{ product.product_name }}</h3>
        </router-link>
        <p>Price: ${{ product.price }}</p>
        <p>Category: {{ product.category.category_name }}</p>
        <p>Sold: {{ product.sold ? 'Yes' : 'No' }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchProducts } from '../api';

const products = ref([]);
const error = ref(null);

const loadProducts = async () => {
  try {
    const response = await fetchProducts({ sold: false }); // Fetch available (not sold) products
    products.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to fetch products.';
  }
};

onMounted(() => {
  loadProducts();
});
</script>

<style scoped>
.product-list {
  max-width: 800px;
  margin: 20px auto;
  padding: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.product-item {
  margin-bottom: 1rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;
}
</style>
