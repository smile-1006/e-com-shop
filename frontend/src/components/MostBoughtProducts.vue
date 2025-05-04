<template>
  <div class="most-bought-products">
    <h2>Most Bought Products</h2>
    <ul>
      <li v-for="product in mostBoughtProducts" :key="product.id" class="product-item">
        <h3>{{ product.product_name }}</h3>
        <p>Price: ${{ product.price }}</p>
        <p>Purchased Quantity: {{ product.total_quantity }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'MostBoughtProducts',
  computed: {
    ...mapGetters('mostBoughtProducts', ['mostBoughtProducts']),
  },
  created() {
    this.loadMostBoughtProducts();
  },
  methods: {
    ...mapActions('mostBoughtProducts', ['loadMostBoughtProducts']),
  },
};
</script>

<style scoped>
.most-bought-products {
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.product-item {
  margin-bottom: 1rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;
}
</style>
