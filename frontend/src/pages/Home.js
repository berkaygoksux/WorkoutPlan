// src/pages/Home.js

import React, { useEffect, useState } from 'react';
import './Home.css';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [nextPlan, setNextPlan] = useState(null);
  const [userName, setUserName] = useState('User');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    console.log("TOKEN (from localStorage):", token); // Token kontrolü

    if (!token) {
      navigate('/login');
      return;
    }

    const fetchUser = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/user/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setUserName(data.name || 'User');
        }
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    };

    const fetchPlans = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/plans`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setPlans(data);

          const today = new Date();
          const futurePlans = data.filter(p => new Date(p.start_date) >= today);
          const sorted = futurePlans.sort((a, b) => new Date(a.start_date) - new Date(b.start_date));
          if (sorted.length > 0) {
            setNextPlan(sorted[0]);
          }
        } else {
          console.error('Failed to fetch plans');
        }
      } catch (error) {
        console.error('Error fetching plans:', error);
      }
    };

    fetchUser();
    fetchPlans();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="home-wrapper">
      <h1 className="welcome-title">Welcome back, {userName}!</h1>

      <section className="section-box">
        <h2>Today's Workout Plans</h2>
        {plans.length > 0 ? (
          plans
            .filter(plan => {
              const today = new Date().toISOString().split('T')[0];
              return plan.start_date.startsWith(today);
            })
            .map((plan) => (
              <div key={plan.plan_id} className="workout-list">
                <h3>{plan.title}</h3>
                <ul>
                  {plan.exercises.map((ex, idx) => (
                    <li key={idx}>
                      {ex.name} – {ex.sets} sets of {ex.reps} reps
                    </li>
                  ))}
                </ul>
              </div>
            ))
        ) : (
          <p>No plans found.</p>
        )}
      </section>

      <section className="section-box">
        <h2>Your Weekly Stats</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>{plans.length}</h3>
            <p>Workouts</p>
          </div>
          <div className="stat-card">
            <h3>~3h</h3>
            <p>Total Time (est.)</p>
          </div>
        </div>
      </section>

      <section className="section-box">
        <h2>Actions</h2>
        <div className="action-buttons">
          <button onClick={() => navigate('/create-plan')}>Create New Plan</button>
          <button onClick={() => navigate('/plans')}>View All Plans</button>
          <button onClick={() => navigate('/exercises')}>Discover Exercises</button>
        </div>
      </section>

      <section className="section-box">
        <h2>Reminder</h2>
        {nextPlan ? (
          <p>🕒 Your next workout is <strong>{nextPlan.title}</strong> on {new Date(nextPlan.start_date).toLocaleString()}</p>
        ) : (
          <p>No upcoming plans.</p>
        )}
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </section>
    </div>
  );
};

export default Home;
