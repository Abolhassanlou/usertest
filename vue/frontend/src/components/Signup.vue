<template>
    <div class="signup">
      <h2>Sign Up</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div>
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div>
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Sign Up</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    data() {
      return {
        username: '',
        email: '',
        password: '',
        errorMessage: '',
      };
    },
    methods: {
      async submitForm() {
        try {
          const response = await axios.post('/api/signup', {
            username: this.username,
            email: this.email,
            password: this.password,
          });
  
          // Handle successful signup
          this.$router.push('/login');
        } catch (error) {
          this.errorMessage = error.response?.data?.message || 'Something went wrong';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Style your signup form here */
  </style>
  