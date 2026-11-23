
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { fetchUsers, toggleAdmin, deleteUser } from "../store/adminSlice";
import type { AppDispatch, RootState } from "../store";

export default function AdminPage() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { users, isLoading, error } = useSelector((state: RootState) => state.admin);
  const currentUser = useSelector((state: RootState) => state.auth.user);

  // Защита: если не админ — уводим на главную
  useEffect(() => {
    if (currentUser && !currentUser.is_admin) {
      navigate("/");
    }
  }, [currentUser, navigate]);

  // Загрузка списка пользователей
  useEffect(() => {
    if (currentUser?.is_admin) {
      dispatch(fetchUsers());
    }
  }, [dispatch, currentUser]);

  const handleToggleAdmin = async (id: number, current: boolean) => {
    await dispatch(toggleAdmin({ id, is_admin: !current }));
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Удалить пользователя? Все его файлы будут удалены.")) {
      await dispatch(deleteUser(id));
    }
  };

  if (!currentUser?.is_admin) {
    return <p>Доступ запрещён.</p>;
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Управление пользователями</h2>

      {error && <p style={{ color: "red" }}>Ошибка: {error}</p>}
      {isLoading && users.length === 0 && <p>Загрузка...</p>}

      {users.length > 0 && (
        <table border={1} cellPadding={6} style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Логин</th>
              <th>Полное имя</th>
              <th>Email</th>
              <th>Админ</th>
              <th>Файлов</th>
              <th>Размер</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.username}</td>
                <td>{u.full_name}</td>
                <td>{u.email}</td>
                <td>{u.is_admin ? "Да" : "Нет"}</td>
                <td>{u.files_count}</td>
                <td>{u.files_size}</td>
                <td>
                  <Link to={`/files?owner=${u.id}`} style={{ marginRight: 8 }}>
                    Файлы
                  </Link>
                  <button
                    onClick={() => handleToggleAdmin(u.id, u.is_admin)}
                    disabled={u.id === currentUser.id}
                    style={{ marginRight: 8 }}
                  >
                    {u.is_admin ? "Снять админа" : "Сделать админом"}
                  </button>
                  <button
                    onClick={() => handleDelete(u.id)}
                    disabled={u.id === currentUser.id}
                  >
                    Удалить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}