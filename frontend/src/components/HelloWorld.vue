<template>
  <div class="app-wrapper">
    <nav class="top-nav">
      <div class="nav-left">
        <h1 class="logo">Django Ecommerce</h1>
      </div>
      <div class="nav-right">
        <button @click="goToCart" class="nav-button">🛒 Cart ({{ cartItemCount }})</button>
        <button @click="goToSignup" class="nav-button">🔒 Sign Up</button>
        <button @click="goToSignin" class="nav-button">🔑 Sign In</button>
      </div>
    </nav>

    <div class="main-content">
      <aside class="side-nav">
        <h2>Filter Products</h2>
        <div class="filter-group">
          <label>Category</label>
          <select v-model="filters.category">
            <option value="">All</option>
            <option v-for="category in categories" :key="category.id" :value="category.category_name">
              {{ category.category_name }}
            </option>
          </select>
        </div>
        <div class="filter-group">
          <label>Sold Status</label>
          <select v-model="filters.sold">
            <option value="">All</option>
            <option value="true">Sold</option>
            <option value="false">Available</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Min Price ($)</label>
          <input type="number" v-model.number="filters.price_min" min="0" />
        </div>
        <div class="filter-group">
          <label>Max Price ($)</label>
          <input type="number" v-model.number="filters.price_max" min="0" />
        </div>
        <div class="filter-actions">
          <button @click="applyFilters">Apply</button>
          <button @click="clearFilters" class="clear-btn">Clear</button>
        </div>
      </aside>

      <section class="content-area">
        <div class="search-bar">
          <input type="text" v-model="searchQuery" placeholder="🔍 Search products..." @keyup.enter="applyFilters" />
          <button @click="applyFilters">Search</button>
        </div>
        <h2 class="section-heading">Available Products</h2>
        <div class="products-grid">
          <div v-for="product in products" :key="product.id" class="product-card">
            <h3 class="product-name">{{ product.product_name }}</h3>
            <p class="product-price">$ {{ product.price.toFixed(2) }}</p>
            <p class="product-category">Category: {{ product.category.category_name }}</p>
            <div class="product-actions">
              <button @click="viewDescription(product)" class="desc-btn">View Description</button>
              <button @click="addToCart(product)">Add to Cart</button>
            </div>
            <span class="status-badge" :class="product.sold ? 'sold' : 'available'">
              {{ product.sold ? 'Sold Out' : 'In Stock' }}
            </span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { fetchProducts, fetchCategories, addToCart as apiAddToCart, fetchCart } from '../api';
import { useRouter } from 'vue-router';

const router = useRouter();

const products = ref([]);
const categories = ref([]);
const searchQuery = ref('');
const filters = ref({
  category: '',
  sold: '',
  price_min: null,
  price_max: null,
});

const cartItems = ref([]);
const cartProductIds = ref(new Set());

const fetchAllCategories = async () => {
  try {
    const response = await fetchCategories();
    categories.value = response.data;
  } catch (error) {
    console.error('Failed to fetch categories:', error);
  }
};

const fetchFilteredProducts = async () => {
  try {
    const params = {
      search: searchQuery.value,
      category__category_name: filters.value.category || undefined,
      sold: filters.value.sold || undefined,
      price_min: filters.value.price_min || undefined,
      price_max: filters.value.price_max || undefined,
    };
    Object.keys(params).forEach(key => params[key] === undefined && delete params[key]);
    const response = await fetchProducts(params);
    products.value = response.data;
  } catch (error) {
    console.error('Failed to fetch products:', error);
  }
};

const fetchCartItems = async () => {
  try {
    const response = await fetchCart();
    cartItems.value = response.data;
    cartProductIds.value = new Set(cartItems.value.map(item => item.product.id));
  } catch (error) {
    console.error('Failed to fetch cart items:', error);
  }
};

const addToCart = async (product) => {
  if (cartProductIds.value.has(product.id)) {
    alert('Product is already in the cart');
    return;
  }
  try {
    await apiAddToCart(product.id, 1);
    alert(`Added ${product.product_name} to cart.`);
    await fetchCartItems();
  } catch (error) {
    console.error('Failed to add to cart:', error);
    alert('Failed to add to cart.');
  }
};

const applyFilters = () => {
  fetchFilteredProducts();
};

const clearFilters = () => {
  searchQuery.value = '';
  filters.value = {
    category: '',
    sold: '',
    price_min: null,
    price_max: null,
  };
  fetchFilteredProducts();
};

const viewDescription = (product) => {
  alert(`Description: ${product.description || 'No description available.'}`);
};

const goToSignup = () => {
  router.push('/signup');
};

const goToSignin = () => {
  router.push('/signin');
};

const goToCart = () => {
  router.push('/cart');
};

const cartItemCount = computed(() => cartItems.value.length);

onMounted(() => {
  fetchAllCategories();
  fetchFilteredProducts();
});
</script>

<style scoped>
.app-wrapper {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f6f8;
  color: #333;
  min-height: 100vh;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1e90ff;
  padding: 15px 30px;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 1.8rem;
  font-weight: bold;
}

.nav-button {
  margin-left: 20px;
  background: #ffffff22;
  border: 1px solid white;
  color: white;
  border-radius: 6px;
  padding: 8px 14px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.nav-button:hover {
  background-color: #ffffff33;
}

.main-content {
  display: flex;
  padding: 20px;
  gap: 20px;
}

.side-nav {
  width: 260px;
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 0.9rem;
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.filter-actions button {
  padding: 8px 12px;
  border-radius: 6px;
  background-color: #1e90ff;
  border: none;
  color: white;
  cursor: pointer;
}

.clear-btn {
  background-color: #888;
}

.content-area {
  flex: 1;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-bar input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.section-heading {
  margin-bottom: 15px;
  font-size: 1.4rem;
  font-weight: 600;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.product-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  transition: transform 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
}

.product-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.product-price {
  color: #1e90ff;
  font-weight: bold;
  margin-bottom: 5px;
}

.product-category {
  color: #555;
  margin-bottom: 10px;
}

.product-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

button.desc-btn {
  background-color: #6c63ff;
}

.status-badge {
  display: inline-block;
  margin-top: 12px;
  padding: 6px 10px;
  border-radius: 20px;
  color: white;
  font-size: 0.8rem;
  font-weight: bold;
}

.sold {
  background-color: red;
}

.available {
  background-color: green;
}
</style>
