<template>
    <div>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="loginUser">Login</button>
    </div>
  </template>
  
  <script>
  import { login } from "../services/api";
  
  export default {
    data() {
      return { username: "", password: "" };
    },
    methods: {
      async loginUser() {
        const response = await login({ username: this.username, password: this.password });
        localStorage.setItem("token", response.data.access_token);
        this.$router.push("/dashboard");
      },
    },
  };
  </script>
  