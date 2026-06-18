import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function LoginRegister() {
  const { login, register } = useContext(AuthContext);
  const navigate = useNavigate();
  
  const [isLoginTab, setIsLoginTab] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    let result;
    if (isLoginTab) {
      result = await login(username, password);
    } else {
      result = await register(username, email, password);
    }

    setLoading(false);
    if (result.success) {
      navigate('/'); // Redirige al descargador una vez autenticado
    } else {
      setError(result.message);
    }
  };

  return (
    <div className="container auth-page">
      <div className="auth-box">
        <div className="auth-tabs">
          <button 
            className={isLoginTab ? 'active-tab' : ''} 
            onClick={() => { setIsLoginTab(true); setError(''); }}
          >
            Iniciar Sesión
          </button>
          <button 
            className={!isLoginTab ? 'active-tab' : ''} 
            onClick={() => { setIsLoginTab(false); setError(''); }}
          >
            Registrarse
          </button>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="text"
            placeholder="Nombre de usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          
          {!isLoginTab && (
            <input
              type="email"
              placeholder="Correo electrónico"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          )}

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? 'Procesando...' : isLoginTab ? 'Entrar' : 'Crear Cuenta'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginRegister;