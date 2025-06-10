// App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Plans from './pages/Plans';
import Exercises from './pages/Exercises';
import CreatePlan from './pages/CreatePlan';
import Home from './pages/Home';

const App = () => {
  const [token, setToken] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    setToken(storedToken);
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={token ? <Home /> : <Navigate to="/login" />} />
        <Route path="/plans" element={token ? <Plans /> : <Navigate to="/login" />} />
        <Route path="/exercises" element={token ? <Exercises /> : <Navigate to="/login" />} />
        <Route path="/create-plan" element={token ? <CreatePlan /> : <Navigate to="/login" />} />
        <Route path="*" element={<Navigate to={token ? "/home" : "/login"} />} />
      </Routes>
    </Router>
  );
};

export default App;
