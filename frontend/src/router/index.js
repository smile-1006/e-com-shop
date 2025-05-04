import { createRouter, createWebHistory } from 'vue-router';
// import Home from '../views/Home.vue';
// import ProductList from '../views/ProductList.vue';
import Cart from '../views/Cart.vue';
import Order from '../views/Order.vue';
import Signin from '../views/Signin.vue';
import Signup from '../views/Signup.vue';

const routes = [
  // { path: '/', component: Home },
  // { path: '/products', component: ProductList },
  { path: '/cart', component: Cart },
  { path: '/orders', component: Order },
  { path: '/signin', component: Signin },
  { path: '/signup', component: Signup },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
