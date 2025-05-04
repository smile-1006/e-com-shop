<template>
  <div>
    <h1>My Cart</h1>
    <div v-for="item in cartItems" :key="item.id" class="cart-item">
      <h3>{{ item.product.name }}</h3>
      <p>Price: ${{ item.product.price }}</p>
      <div class="quantity-controls">
        <button @click="decreaseQuantity(item)">-</button>
        <span>{{ item.quantity }}</span>
        <button @click="increaseQuantity(item)">+</button>
      </div>
      <button @click="removeItem(item)">Remove</button>
    </div>
    <div class="cart-summary">
      <h2>Cart Summary</h2>
      <p>Total Items: {{ totalItems }}</p>
      <p>Total Price: ${{ totalPrice.toFixed(2) }}</p>
      <button @click="proceedToCheckout" :disabled="cartItems.length === 0">Proceed to Checkout</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { fetchCart, increaseCartQuantity, decreaseCartQuantity, removeFromCart } from '../api';
import { useRouter } from 'vue-router';

const cartItems = ref([]);
const router = useRouter();

const loadCart = async () => {
  try {
    const response = await fetchCart();
    cartItems.value = response.data;
  } catch (error) {
    console.error('Failed to load cart:', error);
  }
};

const increaseQuantity = async (item) => {
  try {
    await increaseCartQuantity(item.id);
    await loadCart();
  } catch (error) {
    console.error('Failed to increase quantity:', error);
  }
};

const decreaseQuantity = async (item) => {
  try {
    await decreaseCartQuantity(item.id);
    await loadCart();
  } catch (error) {
    console.error('Failed to decrease quantity:', error);
  }
};

const removeItem = async (item) => {
  try {
    await removeFromCart(item.id);
    await loadCart();
  } catch (error) {
    console.error('Failed to remove item:', error);
  }
};

const totalItems = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.quantity, 0);
});

const totalPrice = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
});

const proceedToCheckout = () => {
  router.push('/orders');
};

onMounted(() => {
  loadCart();
});
</script>

<script>
export default {
  name: 'UserCart'
}
</script>

<style scoped>
.cart-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.quantity-controls button {
  padding: 5px 10px;
  background-color: #42b983;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.quantity-controls button:hover {
  background-color: #369870;
}

.cart-summary {
  margin-top: 20px;
  border-top: 2px solid #42b983;
  padding-top: 10px;
}

.cart-summary button {
  padding: 10px 20px;
  background-color: #42b983;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}

.cart-summary button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
