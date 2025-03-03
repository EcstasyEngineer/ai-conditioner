import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from '../components/LoginPage';
import MainDashboard from '../components/MainDashboard';
import LineCollectionEditor from '../components/LineCollectionEditor';
import ContactUsPage from '../components/ContactUsPage';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/dashboard" element={<MainDashboard />} />
        <Route path="/line-collection-editor" element={<LineCollectionEditor />} />
        <Route path="/contact" element={<ContactUsPage />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
