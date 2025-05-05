<template>
  <div class="product-detail-container" v-if="product">
    <h1>{{ product.product_name }}</h1>
    <p>Price: ${{ product.price }}</p>
    <p>Category: {{ product.category.category_name }}</p>
    <p>Description: {{ product.description }}</p>
    <p>Sold: {{ product.sold ? 'Yes' : 'No' }}</p>
  </div>
  <div v-else>
    <p>Loading product details...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getProductByName } from '../api';

const route = useRoute();
const product = ref(null);
const error = ref(null);

const fetchProductByName = async (name) => {
  try {
    const response = await getProductByName(name);
    product.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to fetch product details.';
  }
};

onMounted(() => {
  const productName = route.params.name;
  if (productName) {
    fetchProductByName(productName);
  }
});
</script>

<style scoped>
.product-detail-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
