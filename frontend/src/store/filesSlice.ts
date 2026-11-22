import { createSlice, createAsyncThunk, type PayloadAction } from "@reduxjs/toolkit";
import { api } from "../api/client";

export type FileItem = {
  id: number;
  owner: number;
  owner_username: string;
  file_name: string;
  size: number;
  comment: string;
  uploaded_at: string;
  last_downloaded_at: string | null;
  share_token: string;
  share_url: string;
};

type FilesState = {
  files: FileItem[];
  isLoading: boolean;
  error: string | null;
};

const initialState: FilesState = {
  files: [],
  isLoading: false,
  error: null,
};

// Получить список файлов (свой или чужой, если передан ownerId)
export const fetchFiles = createAsyncThunk(
  "files/fetchFiles",
  async (ownerId: number | undefined = undefined) => {
    const url = ownerId ? `/api/files/?owner=${ownerId}` : "/api/files/";
    const response = await api.get(url);
    return response.data as FileItem[];
  }
);

// Загрузить файл
export const uploadFile = createAsyncThunk(
  "files/uploadFile",
  async ({ file, comment }: { file: File; comment: string }) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("comment", comment);
    const response = await api.post("/api/files/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data as FileItem;
  }
);

// Удалить файл
export const deleteFile = createAsyncThunk(
  "files/deleteFile",
  async (id: number) => {
    await api.delete(`/api/files/${id}/`);
    return id;
  }
);

// Переименовать / изменить комментарий
export const updateFile = createAsyncThunk(
  "files/updateFile",
  async ({ id, data }: { id: number; data: { file_name?: string; comment?: string } }) => {
    const response = await api.patch(`/api/files/${id}/`, data);
    return response.data as FileItem;
  }
);

const filesSlice = createSlice({
  name: "files",
  initialState,
  reducers: {
    clearFilesError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchFiles
      .addCase(fetchFiles.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchFiles.fulfilled, (state, action: PayloadAction<FileItem[]>) => {
        state.isLoading = false;
        state.files = action.payload;
      })
      .addCase(fetchFiles.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || "Ошибка загрузки файлов";
      })
      // uploadFile
      .addCase(uploadFile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(uploadFile.fulfilled, (state, action: PayloadAction<FileItem>) => {
        state.isLoading = false;
        // Добавляем новый файл в начало списка
        state.files.unshift(action.payload);
      })
      .addCase(uploadFile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || "Ошибка загрузки файла";
      })
      // deleteFile
      .addCase(deleteFile.fulfilled, (state, action: PayloadAction<number>) => {
        state.files = state.files.filter((f) => f.id !== action.payload);
      })
      // updateFile
      .addCase(updateFile.fulfilled, (state, action: PayloadAction<FileItem>) => {
        const index = state.files.findIndex((f) => f.id === action.payload.id);
        if (index !== -1) {
          state.files[index] = action.payload;
        }
      });
  },
});

export const { clearFilesError } = filesSlice.actions;
export default filesSlice.reducer;