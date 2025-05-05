<template>
  <nav class="nav-bar">
    <ul class="category-list">
      <li v-for="category in categories" :key="category.id">
        <a href="#" @click.prevent="selectCategory(category.category_name)">
          {{ category.category_name }}
        </a>
      </li>
    </ul>
    <div class="auth-links">
      <template v-if="isAuthenticated">
        <span>Welcome, {{ fullName }}</span>
        <button @click="logout">Logout</button>
      </template>
      <template v-else>
        <router-link to="/signin">Sign In</router-link>
        <router-link to="/signup">Sign Up</router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { fetchCategories } from '../api';
import { useStore } from 'vuex';

const categories = ref([]);
const store = useStore();

const isAuthenticated = computed(() => store.getters['user/isAuthenticated']);
const fullName = computed(() => store.getters['user/full_name']);

const logout = () => {
  store.dispatch('user/logout');
};

const selectCategory = (categoryName) => {
  // Emit event to parent to filter products by category
  // This can be handled via emits or a global store
  // For now, just log
  console.log('Selected category:', categoryName);
};

const loadCategories = async () => {
  try {
    const response = await fetchCategories();
    categories.value = response.data;
  } catch (error) {
    console.error('Failed to load categories:', error);
  }
};

onMounted(() => {
  loadCategories();
});
</script>

<script>
export default {
  name: 'AppNavbar'
}
</script>

<style scoped>
.nav-bar {
  background-color: #42b983;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-list {
  list-style: none;
  display: flex;
  gap: 15px;
  margin: 0;
  padding: 0;
}

.category-list li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.category-list li a:hover {
  text-decoration: underline;
}

.auth-links {
  display: flex;
  gap: 15px;
  align-items: center;
  color: white;
}

.auth-links a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.auth-links a:hover {
  text-decoration: underline;
}

.auth-links button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-weight: bold;
  padding: 0;
}
</style>
