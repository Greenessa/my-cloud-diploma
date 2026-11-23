
import { useState, type SubmitEvent } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/client";
import { fetchMe } from "../store/authSlice";
import type { AppDispatch, RootState } from "../store";

export default function RegisterPage() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { isLoading } = useSelector((state: RootState) => state.auth);

  const [form, setForm] = useState({
    username: "",
    full_name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    try {
      // Регистрация автоматически логинит пользователя (на бэкенде вызывается login)
      await api.post("/api/auth/register/", form);
      await dispatch(fetchMe());
      navigate("/files");
    } catch (err: any) {
      // Если бэкенд вернул ошибки валидации в JSON — показываем их
      if (err.response?.data) {
        const messages = Object.values(err.response.data)
          .flat()
          .join(" ");
        setError(messages);
      } else {
        setError("Ошибка регистрации. Попробуйте ещё раз.");
      }
    }
  };

  return (
    <div style={{ padding: 20, maxWidth: 400 }}>
      <h2>Регистрация</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Логин (латиница, от 4 до 20 символов)"
          value={form.username}
          onChange={handleChange}
          required
        />
        <br /><br />
        <input
          type="text"
          name="full_name"
          placeholder="Полное имя"
          value={form.full_name}
          onChange={handleChange}
          required
        />
        <br /><br />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <br /><br />
        <input
          type="password"
          name="password"
          placeholder="Пароль (мин. 6 симв., заглавная, цифра, спецсимвол)"
          value={form.password}
          onChange={handleChange}
          required
        />
        <br /><br />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Регистрация..." : "Зарегистрироваться"}
        </button>
      </form>
      {error && <p style={{ color: "red" }}>Ошибка: {error}</p>}
      <p>
        Уже есть аккаунт? <Link to="/login">Войти</Link>
      </p>
    </div>
  );
}