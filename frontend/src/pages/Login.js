import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    // Şimdilik sahte giriş (backend yok)
    localStorage.setItem('user_email', email);
    navigate('/');
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
        </div>
      </div>
    </div>
  );
};

export default Login;
