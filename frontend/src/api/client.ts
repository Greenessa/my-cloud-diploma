import axios from "axios";

// Базовый URL бэкенда. В dev-режиме — Django на порту 8000.
// const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const API_BASE = "";

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,  // Отправлять cookie сессии
});

// Функция для получения CSRF-токена из cookie
function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? decodeURIComponent(match[2]) : null;
}

// автоматически добавляет CSRF-токен к небезопасным методам
api.interceptors.request.use((config) => {
  const csrftoken = getCookie("csrftoken");
  if (csrftoken && ["post", "put", "patch", "delete"].includes(config.method?.toLowerCase() || "")) {
    config.headers["X-CSRFToken"] = csrftoken;
  }
  return config;
});