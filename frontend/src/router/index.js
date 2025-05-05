import { createRouter, createWebHistory } from 'vue-router';
// import Home from '../views/Home.vue';
// import ProductList from '../views/ProductList.vue';
import Cart from '../views/Cart.vue';
import Order from '../views/Order.vue';
import Signin from '../views/Signin.vue';
import Signup from '../views/Signup.vue';
import UserSignin from '../views/UserSignin.vue';
import ProductDetail from '../views/ProductDetail.vue';

const routes = [
  // { path: '/', component: Home },
  // { path: '/products', component: ProductList },
  { path: '/cart', component: Cart },
  { path: '/orders', component: Order },
  { path: '/signin', component: UserSignin },
  { path: '/signup', component: Signup },
  { path: '/signin', component: Signin },
  { path: '/product/:name', component: ProductDetail, props: true },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

