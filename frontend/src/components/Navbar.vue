<template>
  <nav class="nav-bar">
    <ul class="category-list">
      <li v-for="category in categories" :key="category.id">
        <a href="#" @click.prevent="selectCategory(category.category_name)">
          {{ category.category_name }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchCategories } from '../api';

const categories = ref([]);

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
</style>
