import axios from 'axios';

const api = axios.create({
  baseURL: 'https://e-com-shop.onrender.com/',
});

export default api;

export function sendOtp(mobile) {
  return api.post('send-otp/', { mobile });
}

export function verifyOtp(mobile, otp) {
  return api.post('verify-otp/', { mobile, otp });
}

export function fetchMostBoughtProducts() {
  return api.get('products/most_bought/');
}

export function fetchProducts(params) {
  return api.get('products/', { params });
}

export function fetchCategories() {
  return api.get('categories/');
}

export function fetchCart() {
  return api.get('cart/');
}

export function addToCart(productId, quantity = 1) {
  return api.post('cart/add_to_cart/', { product: productId, quantity });
}

export function increaseCartQuantity(cartItemId) {
  return api.post(`cart/${cartItemId}/increase_quantity/`);
}

export function decreaseCartQuantity(cartItemId) {
  return api.post(`cart/${cartItemId}/decrease_quantity/`);
}

export function removeFromCart(cartItemId) {
  return api.delete(`cart/${cartItemId}/remove_from_cart/`);
}
