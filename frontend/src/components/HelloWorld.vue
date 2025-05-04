<template>
  <div>
    <nav class="top-nav">
      <div class="nav-left">
        <h1>Django Ecommerce</h1>
      </div>
      <div class="nav-right">
        <button @click="goToCart" class="nav-button">Cart ({{ cartItemCount }})</button>
        <button @click="goToSignup" class="nav-button">Sign Up</button>
        <button @click="goToSignin" class="nav-button">Sign In</button>
      </div>
    </nav>
    <div class="main-content">
      <aside class="side-nav">
        <h2>Filters</h2>
        <div class="filter-group">
          <label>Category:</label>
          <select v-model="filters.category">
            <option value="">All</option>
            <option v-for="category in categories" :key="category.id" :value="category.category_name">
              {{ category.category_name }}
            </option>
          </select>
        </div>
        <div class="filter-group">
          <label>Sold:</label>
          <select v-model="filters.sold">
            <option value="">All</option>
            <option value="true">Sold</option>
            <option value="false">Available</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Price Min:</label>
          <input type="number" v-model.number="filters.price_min" min="0" />
        </div>
        <div class="filter-group">
          <label>Price Max:</label>
          <input type="number" v-model.number="filters.price_max" min="0" />
        </div>
        <div class="filter-group">
          <button @click="applyFilters">Apply Filters</button>
          <button @click="clearFilters">Clear Filters</button>
        </div>
      </aside>
      <section class="content-area">
        <div class="search-bar">
          <input type="text" v-model="searchQuery" placeholder="Search products..." @keyup.enter="applyFilters" />
          <button @click="applyFilters">Search</button>
        </div>
        <h2>Product List</h2>
        <div class="products-grid">
          <div v-for="product in products" :key="product.id" class="product-card">
            <h3>{{ product.product_name }}</h3>
            <p>Price: ${{ product.price }}</p>
            <p>Category: {{ product.category.category_name }}</p>
            <button @click="viewDescription(product)">View Description</button>
            <button @click="addToCart(product)">Add to Cart</button>
            <p>
              <span
                class="sale-badge"
                :class="product.sold ? 'sold' : 'available'"
              >
                {{ product.sold ? 'Sold' : 'Available' }}
              </span>
            </p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue';
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
.top-nav {
  display: flex;
  justify-content: space-between;
  background-color: #42b983;
  padding: 10px 20px;
  color: white;
}

.nav-left h1 {
  margin: 0;
}

.nav-right button.nav-button {
  color: white;
  margin-left: 15px;
  background: none;
  border: none;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
}

.nav-right button.nav-button:hover {
  text-decoration: underline;
}

.main-content {
  display: flex;
  margin-top: 20px;
}

.side-nav {
  width: 220px;
  padding: 15px;
  border-right: 1px solid #ddd;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 5px;
  box-sizing: border-box;
}

.filter-group button {
  margin-right: 10px;
  padding: 8px 12px;
  background-color: #42b983;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.filter-group button:hover {
  background-color: #369870;
}

.content-area {
  flex-grow: 1;
  padding: 15px;
}

.search-bar {
  margin-bottom: 15px;
}

.search-bar input {
  padding: 8px;
  width: 250px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.sale-badge {
  padding: 5px 10px;
  border-radius: 12px;
  color: white;
  font-weight: bold;
}

.sold {
  background-color: red;
}

.available {
  background-color: green;
}

button {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #42b983;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #369870;
}
</style>
