
import { createSlice, createAsyncThunk, type PayloadAction } from "@reduxjs/toolkit";
import { api } from "../api/client";

export type User = {
    id: number;
    username: string;
    full_name: string;
    email: string;
    is_admin: boolean;
    storage_path: string;
  };
  
  type AuthState = {
    user: User | null;
    isLoading: boolean;
    error: string | null;
  };
  
  const initialState: AuthState = {
    user: null,
    isLoading: true,
    error: null,
  };

  // Thunk для получения текущего пользователя
export const fetchMe = createAsyncThunk("auth/fetchMe", async () => {
    const response = await api.get("/api/auth/me/");
    return response.data as User;
  });
  
  // Thunk для входа
  export const login = createAsyncThunk(
    "auth/login",
    async (credentials: { username: string; password: string }) => {
      const response = await api.post("/api/auth/login/", credentials);
      return response.data as User;
    }
  );
  
  // Thunk для выхода
  export const logout = createAsyncThunk("auth/logout", async () => {
    await api.post("/api/auth/logout/");
  });
  
  const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
      clearError(state) {
        state.error = null;
      },
    },
    extraReducers: (builder) => {
      builder
        // fetchMe
        .addCase(fetchMe.pending, (state) => {
          state.isLoading = true;
        })
        .addCase(fetchMe.fulfilled, (state, action: PayloadAction<User>) => {
          state.isLoading = false;
          state.user = action.payload;
        })
        .addCase(fetchMe.rejected, (state) => {
          state.isLoading = false;
          state.user = null;
        })
        // login
        .addCase(login.pending, (state) => {
          state.isLoading = true;
          state.error = null;
        })
        .addCase(login.fulfilled, (state, action: PayloadAction<User>) => {
          state.isLoading = false;
          state.user = action.payload;
        })
        .addCase(login.rejected, (state, action) => {
          state.isLoading = false;
          state.error = action.error.message || "Ошибка входа";
        })
        // logout
        .addCase(logout.fulfilled, (state) => {
          state.user = null;
        });
    },
  });
  
  export const { clearError } = authSlice.actions;
  export default authSlice.reducer;