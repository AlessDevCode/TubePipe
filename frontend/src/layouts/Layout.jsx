import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Layout({ children }) {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="layout-container">
      <nav className="navbar">
        <Link to="/" className="navbar-logo">TubePipe 🚀</Link>
        <ul className="navbar-links">
          <li><Link to="/">Descargador</Link></li>
          {user ? (
            <>
              <li><Link to="/profile">Historial</Link></li>
              <li className="user-status">
                <span>Hola, <strong>{user.username}</strong></span>
                <button onClick={logout} className="btn-logout">Salir</button>
              </li>
            </>
          ) : (
            <li><Link to="/login" className="btn-login-nav">Iniciar Sesión</Link></li>
          )}
        </ul>
      </nav>
      <main className="main-content">{children}</main>
    </div>
  );
}

export default Layout;