import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
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
