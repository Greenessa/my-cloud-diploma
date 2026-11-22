import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div style={{ padding: 20 }}>
      <h1>☁️ My Cloud</h1>
      <p>Облачное хранилище файлов.</p>
      <p>
        <Link to="/login">Войти</Link> | <Link to="/register">Регистрация</Link>
      </p>
    </div>
  );
}