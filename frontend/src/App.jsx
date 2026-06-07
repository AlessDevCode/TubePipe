import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState('mp4'); 
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const API_URL = 'http://127.0.0.1:8000/api';

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/history/`);
      setHistory(response.data);
    } catch (error) {
      console.error("Error al consultar el historial:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // MODIFICADO EN FASE 3: Lógica dinámica para la petición y manejo del Blob
  const handleDownload = async (e) => {
    e.preventDefault();
    if (!url) return;

    setDownloading(true);
    try {
      // 1. Enviamos la URL junto con el formato seleccionado ('mp4' o 'mp3') al Backend
      const response = await axios.post(
        `${API_URL}/download/`, 
        { url, format }, // <-- El JSON ahora incluye el formato elegido
        { responseType: 'blob' } // Mantenemos la recepción del binario bruto
      );
      
      // 2. Procesamos el Blob binario
      const blob = new Blob([response.data]);
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      
      // 3. Asignamos dinámicamente la extensión correcta al archivo descargado en el navegador
      const fileExtension = format === 'mp3' ? 'mp3' : 'mp4';
      const filePrefix = format === 'mp3' ? 'audio_descargado' : 'video_descargado';
      link.download = `${filePrefix}.${fileExtension}`; 
      
      // Ejecutamos el clic fantasma para iniciar la descarga del usuario
      link.click();

      // Limpieza y actualización
      setUrl(''); 
      fetchHistory(); 
    } catch (error) {
      console.error("Error durante la descarga:", error);
      alert("Hubo un error al procesar la descarga. Verifica que la URL sea válida y tengas FFmpeg configurado.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="container">
      <h1>TubePipe 🚀</h1>
      <p className="subtitle">Descarga videos de YouTube y gestiona tu historial</p>

      <section className="form-section">
        <form onSubmit={handleDownload}>
          <input
            type="url"
            placeholder="Pega la URL de YouTube aquí..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={downloading}
            required
          />

          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            disabled={downloading}
            className="format-select"
          >
            <option value="mp4">Video (MP4)</option>
            <option value="mp3">Audio (MP3)</option>
          </select>

          <button type="submit" disabled={downloading}>
            {downloading ? 'Descargando...' : 'Descargar'}
          </button>
        </form>
      </section>

      <section className="history-section">
        <h2>Historial de Descargas</h2>
        {loading ? (
          <p>Cargando historial...</p>
        ) : history.length === 0 ? (
          <p>No hay descargas registradas aún.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Título / URL</th>
                <th>Duración</th>
                <th>Estado</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td className="url-cell">{item.title || item.url}</td>
                  <td>{item.duration ? `${Math.round(item.duration / 60)} min` : '-'}</td>
                  <td>
                    <span className={`badge ${item.status}`}>
                      {item.status === 'completed' ? 'Completado' : item.status === 'pending' ? 'Pendiente' : 'Fallido'}
                    </span>
                  </td>
                  <td>{new Date(item.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}

export default App;