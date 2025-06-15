import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { shoppingListAPI } from '../../api';

export const getShoppingList = createAsyncThunk(
  'shoppingList/getShoppingList',
  async () => {
    const response = await shoppingListAPI.getShoppingList();
    return response.data;
  }
);

export const addToShoppingList = createAsyncThunk(
  'shoppingList/addToShoppingList',
  async (id) => {
    const response = await shoppingListAPI.addToShoppingList(id);
    return response.data;
  }
);

export const removeFromShoppingList = createAsyncThunk(
  'shoppingList/removeFromShoppingList',
  async (id) => {
    await shoppingListAPI.removeFromShoppingList(id);
    return id;
  }
);

export const downloadShoppingList = createAsyncThunk(
  'shoppingList/downloadShoppingList',
  async () => {
    const response = await shoppingListAPI.downloadShoppingList();
    return response.data;
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
};

const shoppingListSlice = createSlice({
  name: 'shoppingList',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getShoppingList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getShoppingList.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(getShoppingList.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(addToShoppingList.fulfilled, (state, action) => {
        state.items.push(action.payload);
      })
      .addCase(removeFromShoppingList.fulfilled, (state, action) => {
        state.items = state.items.filter(item => item.id !== action.payload);
      });
  },
});

export const { clearError } = shoppingListSlice.actions;
export default shoppingListSlice.reducer; 