import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import ProductList from '../views/ProductList.vue';
import Cart from '../views/Cart.vue';
import Order from '../views/Order.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/products', component: ProductList },
  { path: '/cart', component: Cart },
  { path: '/orders', component: Order },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
