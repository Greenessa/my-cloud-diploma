import { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import { useDispatch } from "react-redux";
import { fetchMe } from "./store/authSlice";
import type { AppDispatch } from "./store";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import FilesPage from "./pages/FilesPage";
import AdminPage from "./pages/AdminPage";

export default function App() {
  const dispatch = useDispatch<AppDispatch>();

  // При загрузке приложения проверяем, залогинен ли пользователь
  useEffect(() => {
    dispatch(fetchMe());
  }, [dispatch]);

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/files" element={<FilesPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </>
  );
}