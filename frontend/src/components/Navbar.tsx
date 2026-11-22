import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../store/authSlice";
import type { AppDispatch, RootState } from "../store";

export default function Navbar() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const user = useSelector((state: RootState) => state.auth.user);

  const handleLogout = async () => {
    await dispatch(logout());
    navigate("/");
  };

  return (
    <nav style={{ padding: 10, background: "#eee", marginBottom: 20 }}>
      <Link to="/">Главная</Link>{" "}
      {user ? (
        <>
          <Link to="/files">Мои файлы</Link>{" "}
          {user.is_admin && <Link to="/admin">Админка</Link>}{" "}
          <span>Привет, {user.username}!</span>{" "}
          <button onClick={handleLogout}>Выйти</button>
        </>
      ) : (
        <>
          <Link to="/login">Войти</Link>{" "}
          <Link to="/register">Регистрация</Link>
        </>
      )}
    </nav>
  );
}