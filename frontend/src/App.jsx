import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Layout from './layouts/Layout';
import Home from './pages/Home';
import Profile from './pages/Profile';
import LoginRegister from './pages/LoginRegister';
import './App.css';

function AppRoutes() {
  const { user, authLoading } = useContext(AuthContext);

  if (authLoading) {
    return <div className="container"><h1>Cargando TubePipe...</h1></div>;
  }

  return (
    <Routes>
      {/* El descargador principal requiere login obligatorio */}
      <Route path="/" element={user ? <Home /> : <Navigate to="/login" />} />
      
      {/* Historial privado */}
      <Route path="/profile" element={user ? <Profile /> : <Navigate to="/login" />} />
      
      {/* Login y Registro */}
      <Route path="/login" element={!user ? <LoginRegister /> : <Navigate to="/" />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Layout>
          <AppRoutes />
        </Layout>
      </Router>
    </AuthProvider>
  );
}

export default App;