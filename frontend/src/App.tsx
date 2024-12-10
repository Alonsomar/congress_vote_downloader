import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DiputadosPage from './pages/DiputadosPage';
import MainLayout from './components/layout/MainLayout';

function App() {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/" element={<DiputadosPage />} />
          <Route path="/diputados" element={<DiputadosPage />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;
