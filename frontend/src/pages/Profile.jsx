import React, { useState, useEffect } from 'react';
import API from '../api';

function Profile() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [actionId, setActionId] = useState(null); // Para loader por cada fila

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await API.get('/history/');
      setHistory(response.data);
    } catch (error) {
      console.error("Error al consultar el historial:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("¿Seguro que quieres eliminar este registro de tu panel?")) return;
    try {
      await API.delete(`/history/${id}/`);
      setHistory(history.filter(item => item.id !== id));
    } catch (error) {
      alert("No se pudo eliminar el registro.");
    }
  };

  const handleRedownload = async (url, title) => {
    setActionId(url);
    try {
      // Re-ejecuta la descarga mandando el formato mp4 por defecto de forma segura
      const response = await API.post('/download/', { url, format: 'mp4' }, { responseType: 'blob' });
      const blob = new Blob([response.data]);
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `${title || 'video_remanente'}.mp4`;
      link.click();
    } catch (error) {
      alert("Error al intentar descargar de nuevo.");
    } finally {
      setActionId(null);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="container">
      <h1>Mi Panel de Usuario 👤</h1>
      <p className="subtitle">Aquí se muestra únicamente el historial multimedia vinculado a tu cuenta.</p>

      <section className="history-section">
        <h2>Tus Descargas</h2>
        {loading ? (
          <p>Cargando historial privado...</p>
        ) : history.length === 0 ? (
          <p>No tienes descargas registradas todavía.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Título / URL</th>
                <th>Estado</th>
                <th>Fecha</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td className="url-cell"><strong>{item.title || "Procesando..."}</strong><br/><small>{item.url}</small></td>
                  <td>
                    <span className={`badge ${item.status}`}>{item.status}</span>
                  </td>
                  <td>{new Date(item.created_at).toLocaleDateString()}</td>
                  <td>
                    <div className="actions-cell">
                      <button 
                        onClick={() => handleRedownload(item.url, item.title)}
                        className="btn-redownload"
                        disabled={actionId === item.url}
                      >
                        {actionId === item.url ? '...' : 'Descargar'}
                      </button>
                      <button 
                        onClick={() => handleDelete(item.id)}
                        className="btn-delete-row"
                      >
                        Eliminar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}

export default Profile;