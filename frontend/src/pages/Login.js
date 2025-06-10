// src/pages/Login.js

import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './Login.css';

const Login = () => {
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
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user_email', email);
        navigate('/home');
      } else {
        const err = await response.json();
        setError(err.detail || 'Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('An unexpected error occurred.');
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-left">
        <img
          src="/images/gym.jpg"
          alt="Workout Visual"
          className="login-image"
        />
      </div>
      <div className="login-right">
        <div className="logo-container">
          <img src="/images/logo.png" alt="WorkoutPlan Logo" className="logo-image" />
        </div>
        <h1 className="app-title">Welcome to WorkoutPlan</h1>
        <div className="login-container">
          <h2>Login</h2>
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
