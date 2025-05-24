import React from 'react';
import './Home.css';

const Home = () => {
  const userEmail = localStorage.getItem('user_email') || 'User';

  return (
    <div className="home-wrapper">
      <h1 className="welcome-title">Welcome back, {userEmail}!</h1>

      {/* Bugünkü planlar */}
      <section className="section-box">
        <h2>Today's Workout Plan</h2>
        <ul className="workout-list">
          <li>Push Ups – 4 sets of 15 reps</li>
          <li>Squats – 3 sets of 20 reps</li>
          <li>Plank – 3 rounds of 60 sec</li>
        </ul>
      </section>

      {/* İstatistik kutuları */}
      <section className="section-box">
        <h2>Your Weekly Stats</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>5</h3>
            <p>Workouts</p>
          </div>
          <div className="stat-card">
            <h3>3h 20m</h3>
            <p>Total Time</p>
          </div>
        </div>
      </section>

      {/* Eylem butonları */}
      <section className="section-box">
        <h2>Actions</h2>
        <div className="action-buttons">
          <button>Create New Plan</button>
          <button>View All Plans</button>
          <button>Discover Exercises</button>
        </div>
      </section>

      {/* Bildirim ve çıkış */}
      <section className="section-box">
        <h2>Reminder</h2>
        <p>🕒 Leg Day tomorrow at 09:00</p>
        <button className="logout-button" onClick={() => {
          localStorage.clear();
          window.location.href = "/login";
        }}>Logout</button>
      </section>
    </div>
  );
};

export default Home;
