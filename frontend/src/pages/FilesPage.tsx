import { useEffect, useState, type ChangeEvent } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useSearchParams } from "react-router-dom";
import {
  fetchFiles,
  uploadFile,
  deleteFile,
  updateFile,
} from "../store/filesSlice";
import type { AppDispatch, RootState } from "../store";

export default function FilesPage() {
  const dispatch = useDispatch<AppDispatch>();
  const { files, isLoading, error } = useSelector((state: RootState) => state.files);
  const user = useSelector((state: RootState) => state.auth.user);
  const [searchParams] = useSearchParams();
  const ownerId = searchParams.get("owner");

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [comment, setComment] = useState("");
  const [copiedId, setCopiedId] = useState<number | null>(null);

  // Загрузка списка файлов при монтировании
  useEffect(() => {
    dispatch(fetchFiles(ownerId ? Number(ownerId) : undefined));
  }, [dispatch, ownerId]);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    await dispatch(uploadFile({ file: selectedFile, comment }));
    setSelectedFile(null);
    setComment("");
    // Сбрасываем input, чтобы можно было выбрать тот же файл снова
    const input = document.getElementById("file-input") as HTMLInputElement;
    if (input) input.value = "";
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Удалить файл?")) {
      await dispatch(deleteFile(id));
    }
  };

  const handleRename = async (id: number, currentName: string) => {
    const newName = prompt("Новое имя файла:", currentName);
    if (newName && newName !== currentName) {
      await dispatch(updateFile({ id, data: { file_name: newName } }));
    }
  };

  const handleCopyLink = async (shareUrl: string, id: number) => {
    await navigator.clipboard.writeText(shareUrl);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>
        {ownerId && user?.is_admin
          ? `Файлы пользователя #${ownerId}`
          : "Мои файлы"}
      </h2>

      {/* Форма загрузки — только для своего хранилища */}
      {!ownerId && (
        <div style={{ marginBottom: 20, padding: 10, border: "1px solid #ccc" }}>
          <h3>Загрузить файл</h3>
          <input id="file-input" type="file" onChange={handleFileChange} />
          <input
            type="text"
            placeholder="Комментарий (необязательно)"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            style={{ marginLeft: 10 }}
          />
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isLoading}
            style={{ marginLeft: 10 }}
          >
            {isLoading ? "Загрузка..." : "Загрузить"}
          </button>
        </div>
      )}

      {error && <p style={{ color: "red" }}>Ошибка: {error}</p>}

      {isLoading && files.length === 0 && <p>Загрузка списка...</p>}

      {!isLoading && files.length === 0 && <p>Файлов пока нет.</p>}

      {files.length > 0 && (
        <table border={1} cellPadding={6} style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>Имя</th>
              <th>Размер, байт</th>
              <th>Комментарий</th>
              <th>Загружен</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {files.map((f) => (
              <tr key={f.id}>
                <td>{f.file_name}</td>
                <td>{f.size}</td>
                <td>{f.comment || "—"}</td>
                <td>{new Date(f.uploaded_at).toLocaleString()}</td>
                <td>
                  <a
                    href={`http://127.0.0.1:8000/api/files/${f.id}/download/`}
                    target="_blank"
                    rel="noreferrer"
                    style={{ marginRight: 8 }}
                  >
                    Скачать
                  </a>
                  {!ownerId && (
                    <>
                      <button onClick={() => handleRename(f.id, f.file_name)}>Переименовать</button>
                      <button onClick={() => handleDelete(f.id)}>Удалить</button>
                    </>
                  )}
                  <button onClick={() => handleCopyLink(f.share_url, f.id)}>
                    {copiedId === f.id ? "Скопировано!" : "Ссылка"}
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