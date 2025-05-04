<template>
  <div>
    <h1>My Orders</h1>
    <button @click="placeOrder" :disabled="cartItems.length === 0">Place Order</button>
    <div v-if="orders.length === 0">
      <p>No orders found.</p>
    </div>
    <div v-else>
      <div v-for="order in orders" :key="order.id" class="order-card">
        <h3>Order #{{ order.id }}</h3>
        <p>Date: {{ order.order_date }}</p>
        <p>Status: {{ order.status }}</p>
        <p>Total Quantity: {{ order.total_quantity }}</p>
        <p>Total Price: ${{ order.total_price.toFixed(2) }}</p>
        <button v-if="order.status === 'Pending'" @click="cancelOrder(order.id)">Cancel Order</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserOrders',
  data() {
    return {
      orders: [],
      cartItems: [],
    };
  },
  methods: {
    async loadOrders() {
      try {
        const userId = 1; // Replace with actual user id logic
        const response = await this.$api.fetchOrders(userId);
        this.orders = response.data;
      } catch (error) {
        console.error('Failed to fetch orders:', error);
      }
    },
    async loadCart() {
      try {
        const response = await this.$api.fetchCart();
        this.cartItems = response.data;
      } catch (error) {
        console.error('Failed to fetch cart:', error);
      }
    },
    async placeOrder() {
      try {
        const userId = 1; // Replace with actual user id logic
        await this.$api.placeOrder(userId);
        alert('Order placed successfully');
        await this.loadOrders();
        await this.loadCart();
      } catch (error) {
        console.error('Failed to place order:', error);
        alert('Failed to place order');
      }
    },
    async cancelOrder(orderId) {
      try {
        await this.$api.cancelOrder(orderId);
        alert('Order cancelled successfully');
        await this.loadOrders();
      } catch (error) {
        console.error('Failed to cancel order:', error);
        alert('Failed to cancel order');
      }
    },
  },
  mounted() {
    this.loadOrders();
    this.loadCart();
  },
};
</script>

<style scoped>
.order-card {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
}
button {
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
