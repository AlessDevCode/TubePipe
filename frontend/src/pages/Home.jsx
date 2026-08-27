import React, { useState } from 'react';
import API from '../api'; // <-- Cambiado a nuestra instancia con JWT interceptor

function Home() {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState('mp4'); 
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async (e) => {
  e.preventDefault();
  if (!url) return;

  setDownloading(true);
  try {
    const response = await API.post(
      '/download/', 
      { url, format }, 
      { responseType: 'blob' }
    );
    
    const blob = new Blob([response.data]);
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    
    let fileExtension = format === 'mp3' ? 'mp3' : format === 'm4a' ? 'm4a' : 'mp4';
    let filePrefix = format === 'mp3' ? 'audio_descargado' : format === 'm4a' ? 'audio_nativo' : 'video_descargado';

    link.download = `${filePrefix}.${fileExtension}`; 
    link.click();

    setUrl(''); 
    alert("¡Descarga procesada y enviada a tu equipo!");
  } catch (error) {
    console.error("Error durante la descarga:", error);
    let errorMessage = "Ocurrió un error inesperado al procesar la descarga.";

    // Extrae el mensaje de error personalizado enviado desde Django en formato Blob
    if (error.response && error.response.data instanceof Blob) {
      try {
        const errorText = await error.response.data.text();
        const errorJson = JSON.parse(errorText);
        if (errorJson.error) {
          errorMessage = errorJson.error;
        }
      } catch (e) {
        // Mantiene el mensaje por defecto si la respuesta no es un JSON válido
      }
    }

    alert(errorMessage);
  } finally {
    setDownloading(false);
  }
};

  return (
    <div className="container">
      <h1>TubePipe 🚀</h1>
      <p className="subtitle">Convierte y descarga contenido multimedia en tiempo real.</p>

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

          <select value={format} onChange={(e) => setFormat(e.target.value)} disabled={downloading} className="format-select">
            <option value="mp4">Video (MP4)</option>
            <option value="mp3">Audio (MP3)</option>
            <option value="m4a">Audio de alta calidad (M4A)</option>
          </select>

          <button type="submit" disabled={downloading}>
            {downloading ? 'Descargando...' : 'Descargar'}
          </button>
        </form>
      </section>
    </div>
  );
}

export default Home;