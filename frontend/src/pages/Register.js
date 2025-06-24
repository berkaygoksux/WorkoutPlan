// src/pages/Register.js
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'user',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert('Registration successful! Please log in.');
        navigate('/login');
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail || 'Registration failed.'}`);
      }
    } catch (error) {
      alert('Network error: Please ensure the server is running.');
    }
  };

  return (
    <div className="register-wrapper">
      <div className="register-left">
        <img src="/images/gym.jpg" alt="Visual" className="register-image" />
      </div>
      <div className="register-right">
        <div className="logo-container">
          <img src="/images/logo.png" alt="Logo" className="logo-image" />
        </div>
        <h1 className="app-title">Create Your Account</h1>
        <div className="register-container">
          <h2>Register</h2>
          <form onSubmit={handleRegister}>
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleChange}
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <select name="role" value={formData.role} onChange={handleChange}>
              <option value="user">User</option>
              <option value="trainer">Trainer</option>
            </select>
            <button type="submit">Register</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;