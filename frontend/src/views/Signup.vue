<template>
  <div class="auth-container">
    <h2>Sign Up</h2>
    <form @submit.prevent="sendOtpHandler">
      <label for="mobile">Mobile Number:</label>
      <input id="mobile" v-model="mobile" type="text" placeholder="+919876543210" required />
      <button type="submit" :disabled="otpSent">Send OTP</button>
    </form>

    <form v-if="otpSent" @submit.prevent="verifyOtpHandler">
      <label for="otp">Enter OTP:</label>
      <input id="otp" v-model="otp" type="text" maxlength="6" required />
      <button type="submit">Verify OTP</button>
    </form>

    <p v-if="message" :class="{ error: error }">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { sendOtp, verifyOtp } from '../api';
import { useRouter } from 'vue-router';

const mobile = ref('');
const otp = ref('');
const otpSent = ref(false);
const message = ref('');
const error = ref(false);
const router = useRouter();

const sendOtpHandler = async () => {
  message.value = '';
  error.value = false;
  try {
    await sendOtp(mobile.value);
    otpSent.value = true;
    message.value = 'OTP sent successfully. Please check your phone.';
  } catch (err) {
    error.value = true;
    message.value = err.response?.data?.error || 'Failed to send OTP.';
  }
};

const verifyOtpHandler = async () => {
  message.value = '';
  error.value = false;
  try {
    await verifyOtp(mobile.value, otp.value);
    message.value = 'OTP verified. You are now logged in.';
    // Redirect to home or product listing page
    router.push('/');
  } catch (err) {
    error.value = true;
    message.value = err.response?.data?.error || 'Failed to verify OTP.';
  }
};
</script>

<script>
export default {
  name: 'UserSignup'
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

button {
  padding: 10px 15px;
  background-color: #42b983;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
