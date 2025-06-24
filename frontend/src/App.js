import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Plans from './pages/Plans';
import WorkoutLogs from './pages/WorkoutLogs';
import Login from './pages/Login';
import Register from './pages/Register';
import CreatePlan from './pages/CreatePlan';
import Exercises from './pages/Exercises';

const PrivateRoute = ({ children, setIsAuthenticated, setUserRole }) => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    setIsAuthenticated(false);
    setUserRole(null);
    return <Navigate to="/login" replace />;
  }
  return children;
};

const App = () => {
  const [userRole, setUserRole] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access_token'));

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setIsAuthenticated(false);
      setUserRole(null);
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <PrivateRoute setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole}>
              <Home userRole={userRole} setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole} />
            </PrivateRoute>
          }
        />
        <Route
          path="/plans"
          element={
            <PrivateRoute setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole}>
              <Plans userRole={userRole} setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole} />
            </PrivateRoute>
          }
        />
        <Route
          path="/logs"
          element={
            <PrivateRoute setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole}>
              <WorkoutLogs userRole={userRole} setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole} />
            </PrivateRoute>
          }
        />
        <Route
          path="/create-plan"
          element={
            <PrivateRoute setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole}>
              <CreatePlan userRole={userRole} setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole} />
            </PrivateRoute>
          }
        />
        <Route
          path="/exercises"
          element={
            <PrivateRoute setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole}>
              <Exercises userRole={userRole} setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole} />
            </PrivateRoute>
          }
        />
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole} />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
};

export default App;