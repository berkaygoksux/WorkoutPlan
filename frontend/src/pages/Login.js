import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './Login.css';
import { jwtDecode } from 'jwt-decode';

const Login = ({ setIsAuthenticated, setUserRole }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user_email', email);
        const decoded = jwtDecode(data.access_token);
        setIsAuthenticated(true);
        setUserRole(decoded.role);
        navigate('/', { replace: true });
      } else {
        const err = await response.json();
        setError(err.detail || 'Login failed. Please check your email and password.');
      }
    } catch (error) {
      setError('Unable to connect to the server. Please try again later.');
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-left">
        <img src="/images/gym.jpg" alt="Workout Visual" className="login-image" />
      </div>
      <div className="login-right">
        <div className="logo-container">
          <img src="/images/logo.png" alt="WorkoutPlan Logo" className="logo-image" />
        </div>
        <h1 className="app-title">Welcome to WorkoutPlan</h1>
        <div className="login-container">
          <h2>Login</h2>
          {error && <p className="error">{error}</p>}
          <form onSubmit={handleLogin}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
          <div className="register-link">
            <p>Don't have an account?</p>
            <button onClick={() => navigate('/register')}>Register</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;