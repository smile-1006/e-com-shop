import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/',
});

export default api;

export function sendOtp(mobile) {
  return api.post('send-otp/', { mobile });
}

export function verifyOtp(mobile, otp) {
  return api.post('verify-otp/', { mobile, otp });
}
