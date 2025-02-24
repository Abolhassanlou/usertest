import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../components/Login.vue';
import Dashboard from '../components/Dashboard.vue';

// Create a simple auth check function
const isAuthenticated = () => {
  // Check if there's an auth token in localStorage
  return !!localStorage.getItem('auth_token');
};

const routes = [
  {
    path: '/',
    component: Home,
  },
  { path: "/signup", 
    component: Signup 
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/dashboard',
    component: Dashboard,
    beforeEnter: (to, from, next) => {
      if (!isAuthenticated()) {
        next('/login'); // Redirect to login if not authenticated
      } else {
        next(); // Allow access to dashboard
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
