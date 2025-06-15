import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (credentials) => api.post('/auth/token/login/', credentials),
  register: (userData) => api.post('/users/', userData),
  logout: () => api.post('/auth/token/logout/'),
  getCurrentUser: () => api.get('/users/me/'),
};

export const recipesAPI = {
  getRecipes: (params) => api.get('/recipes/', { params }),
  getRecipe: (id) => api.get(`/recipes/${id}/`),
  createRecipe: (data) => api.post('/recipes/', data),
  updateRecipe: (id, data) => api.patch(`/recipes/${id}/`, data),
  deleteRecipe: (id) => api.delete(`/recipes/${id}/`),
};

export const favoritesAPI = {
  getFavorites: () => api.get('/recipes/favorites/'),
  addToFavorites: (id) => api.post(`/recipes/${id}/favorite/`),
  removeFromFavorites: (id) => api.delete(`/recipes/${id}/favorite/`),
};

export const shoppingListAPI = {
  getShoppingList: () => api.get('/recipes/shopping-cart/'),
  addToShoppingList: (id) => api.post(`/recipes/${id}/shopping_cart/`),
  removeFromShoppingList: (id) => api.delete(`/recipes/${id}/shopping_cart/`),
  downloadShoppingList: () => api.get('/recipes/download_shopping_cart/'),
};

export const subscriptionsAPI = {
  getSubscriptions: () => api.get('/users/subscriptions/'),
  subscribe: (id) => api.post(`/users/${id}/subscribe/`),
  unsubscribe: (id) => api.delete(`/users/${id}/subscribe/`),
};