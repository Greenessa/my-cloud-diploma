import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";
import type { RootState } from "../store";

type Props = {
  adminOnly?: boolean;
};

export default function ProtectedRoute({ adminOnly = false }: Props) {
  const user = useSelector((state: RootState) => state.auth.user);
  const isLoading = useSelector((state: RootState) => state.auth.isLoading);

  // 1. Если еще идет запрос fetchMe (проверка сессии), показываем загрузку
  if (isLoading) {
    return <p style={{ padding: 20 }}>Загрузка...</p>;
  }

  // 2. Если пользователя нет (не залогинен) — на страницу входа
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // 3. Если страница только для админа, а пользователь не админ — на главную
  if (adminOnly && !user.is_admin) {
    return <Navigate to="/" replace />;
  }

  // 4. Если все проверки пройдены — показываем запрошенную страницу
  return <Outlet />;
}