import React, { useEffect, useState } from 'react';
import './Home.css';
import { useNavigate } from 'react-router-dom';

const Home = ({ userRole, setIsAuthenticated, setUserRole }) => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [nextPlan, setNextPlan] = useState(null);
  const [userName, setUserName] = useState('User');
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setIsAuthenticated(false);
      setUserRole(null);
      navigate('/login', { replace: true });
      return;
    }

    const fetchUser = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/user/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 401) {
          localStorage.removeItem('access_token');
          setIsAuthenticated(false);
          setUserRole(null);
          navigate('/login', { replace: true });
          return;
        }
        if (response.ok) {
          const data = await response.json();
          setUserName(data.name || 'User');
        } else {
          setError('Failed to fetch user information.');
        }
      } catch (error) {
        setError('Unable to connect to the server.');
      }
    };

    const fetchPlans = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/plans`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 401) {
          localStorage.removeItem('access_token');
          setIsAuthenticated(false);
          setUserRole(null);
          navigate('/login', { replace: true });
          return;
        }
        if (response.ok) {
          const data = await response.json();
          setPlans(data);
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          const futurePlans = data.filter((p) => {
            const startDate = new Date(p.start_date);
            return startDate >= today;
          });
          const sorted = futurePlans.sort((a, b) => new Date(a.start_date) - new Date(b.start_date));
          if (sorted.length > 0) {
            setNextPlan(sorted[0]);
          }
        } else {
          setError('Failed to fetch workout plans.');
        }
      } catch (error) {
        setError('Unable to connect to the server.');
      }
    };

    fetchUser();
    fetchPlans();
  }, [navigate, setIsAuthenticated, setUserRole]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    setIsAuthenticated(false);
    setUserRole(null);
    navigate('/login', { replace: true });
  };

  return (
    <div className="home-wrapper">
      <h1 className="welcome-title">Welcome back, {userName}!</h1>
      {error && (
        <p className="error-message" data-testid="error-message">
          {error}
        </p>
      )}

      <section className="section-box">
        <h2>Today's Workout Plans</h2>
        {plans.length > 0 ? (
          plans
            .filter((plan) => {
              const today = new Date().toISOString().split('T')[0];
              return plan.start_date.split('T')[0] === today && today <= plan.end_date.split('T')[0];
            })
            .map((plan) => (
              <div key={plan.plan_id} className="plans">
                <h3>
                  {plan.title} <span className="owner-name">by {plan.owner_name || 'Unknown'}</span>
                </h3>
                <ul>
                  {plan.exercises?.map((ex, idx) => (
                    <li key={idx}>
                      {ex.name || 'Unknown Exercise'} - {ex.sets} sets of {ex.reps} reps
                    </li>
                  ))}
                </ul>
              </div>
            ))
        ) : (
          <p className="no-plans" data-testid="no-plans">
            No plans found for today.
          </p>
        )}
      </section>

      <section className="section-box">
        <h2>Your Weekly Stats</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3 data-testid="workouts-count">{plans.length}</h3>
            <p>Workouts</p>
          </div>
          <div className="stat-card">
            <h3 data-testid="total-time">
              {plans.reduce((total, plan) => total + (plan.exercises?.length || 0) * 0.5, 0)}h
            </h3>
            <p>Total Time (est.)</p>
          </div>
        </div>
      </section>

      <section className="section-box">
        <h2>Actions</h2>
        <div className="action-buttons">
          <button onClick={() => navigate('/create-plan')}>Create New Plan</button>
          <button onClick={() => navigate('/plans')}>View All Plans</button>
          <button onClick={() => navigate('/logs')}>View Workout Logs</button>
          <button onClick={() => navigate('/exercises')}>Discover Exercises</button>
        </div>
      </section>

      <section className="section-box">
        <h2>Reminder</h2>
        {nextPlan ? (
          <p data-testid="next-plan">
            🕒 Your next workout is <strong>{nextPlan.title}</strong> by {nextPlan.owner_name || 'Unknown'} on{' '}
            {new Date(nextPlan.start_date).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        ) : (
          <p data-testid="no-plan">No upcoming workouts.</p>
        )}
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </section>
    </div>
  );
};

export default Home;