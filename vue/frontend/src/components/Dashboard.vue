<template>
    <div>
      <h2>Welcome to Dashboard</h2>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        // Clear the authentication token (or any other session storage)
        localStorage.removeItem('auth_token');
        // Redirect to login
        this.$router.push('/login');
      },
    },
  };
  </script>