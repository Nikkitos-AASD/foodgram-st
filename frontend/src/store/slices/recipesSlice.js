import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { recipesAPI } from '../../api';

export const getRecipes = createAsyncThunk(
  'recipes/getRecipes',
  async (params) => {
    const response = await recipesAPI.getRecipes(params);
    return response.data;
  }
);

export const getRecipe = createAsyncThunk(
  'recipes/getRecipe',
  async (id) => {
    const response = await recipesAPI.getRecipe(id);
    return response.data;
  }
);

export const createRecipe = createAsyncThunk(
  'recipes/createRecipe',
  async (data) => {
    const response = await recipesAPI.createRecipe(data);
    return response.data;
  }
);

export const updateRecipe = createAsyncThunk(
  'recipes/updateRecipe',
  async ({ id, data }) => {
    const response = await recipesAPI.updateRecipe(id, data);
    return response.data;
  }
);

export const deleteRecipe = createAsyncThunk(
  'recipes/deleteRecipe',
  async (id) => {
    await recipesAPI.deleteRecipe(id);
    return id;
  }
);

const initialState = {
  items: [],
  currentRecipe: null,
  loading: false,
  error: null,
  totalPages: 1,
  currentPage: 1,
};

const recipesSlice = createSlice({
  name: 'recipes',
  initialState,
  reducers: {
    clearCurrentRecipe: (state) => {
      state.currentRecipe = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(getRecipes.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getRecipes.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.results;
        state.totalPages = Math.ceil(action.payload.count / 6);
        state.currentPage = action.payload.current_page;
      })
      .addCase(getRecipes.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(getRecipe.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getRecipe.fulfilled, (state, action) => {
        state.loading = false;
        state.currentRecipe = action.payload;
      })
      .addCase(getRecipe.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(createRecipe.fulfilled, (state, action) => {
        state.items.unshift(action.payload);
      })
      .addCase(updateRecipe.fulfilled, (state, action) => {
        const index = state.items.findIndex(item => item.id === action.payload.id);
        if (index !== -1) {
          state.items[index] = action.payload;
        }
        if (state.currentRecipe?.id === action.payload.id) {
          state.currentRecipe = action.payload;
        }
      })
      .addCase(deleteRecipe.fulfilled, (state, action) => {
        state.items = state.items.filter(item => item.id !== action.payload);
        if (state.currentRecipe?.id === action.payload) {
          state.currentRecipe = null;
        }
      });
  },
});

export const { clearCurrentRecipe, clearError } = recipesSlice.actions;
export default recipesSlice.reducer; 