import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { favoritesAPI } from '../../api';

export const getFavorites = createAsyncThunk(
  'favorites/getFavorites',
  async () => {
    const response = await favoritesAPI.getFavorites();
    return response.data;
  }
);

export const addToFavorites = createAsyncThunk(
  'favorites/addToFavorites',
  async (id) => {
    const response = await favoritesAPI.addToFavorites(id);
    return response.data;
  }
);

export const removeFromFavorites = createAsyncThunk(
  'favorites/removeFromFavorites',
  async (id) => {
    await favoritesAPI.removeFromFavorites(id);
    return id;
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const favoritesSlice = createSlice({
  name: 'favorites',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getFavorites.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getFavorites.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(getFavorites.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(addToFavorites.fulfilled, (state, action) => {
        state.items.push(action.payload);
      })
      .addCase(removeFromFavorites.fulfilled, (state, action) => {
        state.items = state.items.filter(item => item.id !== action.payload);
      });
  },
});

export const { clearError } = favoritesSlice.actions;
export default favoritesSlice.reducer; 