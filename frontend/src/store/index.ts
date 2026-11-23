
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./authSlice";
import filesReducer from "./filesSlice";  
import adminReducer from "./adminSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    files: filesReducer, 
    admin: adminReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;