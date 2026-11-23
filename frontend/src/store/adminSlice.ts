import { createSlice, createAsyncThunk, type PayloadAction } from "@reduxjs/toolkit";
import { api } from "../api/client";

export type AdminUser = {
  id: number;
  username: string;
  full_name: string;
  email: string;
  is_admin: boolean;
  storage_path: string;
  files_count: number;
  files_size: number;
};

type AdminState = {
  users: AdminUser[];
  isLoading: boolean;
  error: string | null;
};

const initialState: AdminState = {
  users: [],
  isLoading: false,
  error: null,
};

// Получить список всех пользователей
export const fetchUsers = createAsyncThunk("admin/fetchUsers", async () => {
  const response = await api.get("/api/users/");
  return response.data as AdminUser[];
});

// Изменить флаг администратора
export const toggleAdmin = createAsyncThunk(
  "admin/toggleAdmin",
  async ({ id, is_admin }: { id: number; is_admin: boolean }) => {
    const response = await api.patch(`/api/users/${id}/`, { is_admin });
    return response.data as AdminUser;
  }
);

// Удалить пользователя
export const deleteUser = createAsyncThunk("admin/deleteUser", async (id: number) => {
  await api.delete(`/api/users/${id}/`);
  return id;
});

const adminSlice = createSlice({
  name: "admin",
  initialState,
  reducers: {
    clearAdminError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchUsers
      .addCase(fetchUsers.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action: PayloadAction<AdminUser[]>) => {
        state.isLoading = false;
        state.users = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || "Ошибка загрузки пользователей";
      })
      // toggleAdmin
      .addCase(toggleAdmin.fulfilled, (state, action: PayloadAction<AdminUser>) => {
        const index = state.users.findIndex((u) => u.id === action.payload.id);
        if (index !== -1) {
          state.users[index] = action.payload;
        }
      })
      // deleteUser
      .addCase(deleteUser.fulfilled, (state, action: PayloadAction<number>) => {
        state.users = state.users.filter((u) => u.id !== action.payload);
      });
  },
});

export const { clearAdminError } = adminSlice.actions;
export default adminSlice.reducer;