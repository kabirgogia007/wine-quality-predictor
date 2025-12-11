
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import LandingPage from './pages/Landing';
import Prediction from './pages/Prediction';
import Dashboard from './pages/Dashboard';
import ReportDocs from './pages/Report';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<LandingPage />} />
        <Route path="predict" element={<Prediction />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="report" element={<ReportDocs />} />
      </Route>
    </Routes>
  );
}

export default App;
