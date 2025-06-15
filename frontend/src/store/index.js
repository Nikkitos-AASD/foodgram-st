import { configureStore } from '@reduxjs/toolkit';
import { recipesReducer } from './slices/recipesSlice';
import { authReducer } from './slices/authSlice';
import { favoritesReducer } from './slices/favoritesSlice';
import { shoppingListReducer } from './slices/shoppingListSlice';

export const store = configureStore({
  reducer: {
    recipes: recipesReducer,
    auth: authReducer,
    favorites: favoritesReducer,
    shoppingList: shoppingListReducer,
  },
}); 