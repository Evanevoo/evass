import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import PrivateRoute from '../components/PrivateRoute';
import PublicRoute from '../components/PublicRoute';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
import Customers from '../pages/Customers';
import Cylinders from '../pages/Cylinders';
import Maintenance from '../pages/Maintenance';
import Analytics from '../pages/Analytics';
import BulkUpload from '../pages/BulkUpload';

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route element={<PublicRoute />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>
      <Route element={<PrivateRoute />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/cylinders" element={<Cylinders />} />
        <Route path="/maintenance" element={<Maintenance />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/bulk-upload" element={<BulkUpload />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes; 