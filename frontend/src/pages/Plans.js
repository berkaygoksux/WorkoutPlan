import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Plans.css';

const Plans = () => {
  const [plans, setPlans] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchPlans = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/plans`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.status === 401) {
          navigate('/login');
          return;
        }

        if (!response.ok) {
          throw new Error('Failed to fetch plans');
        }

        const data = await response.json();
        setPlans(data);
      } catch (err) {
        console.error(err);
        setError('Failed to get workout plan');
      }
    };

    fetchPlans();
  }, [navigate]);

  return (
    <div className="plans-wrapper">
      <h1>All Workout Plans</h1>
      {error && <p className="error">{error}</p>}
      <div className="plans-grid">
        {plans.map(plan => (
          <div key={plan.plan_id} className="plan-card">
            <h3>{plan.title}</h3>
            <p><strong>Level:</strong> {plan.level}</p>
            <p><strong>Start:</strong> {new Date(plan.start_date).toLocaleDateString()}</p>
            <p><strong>End:</strong> {new Date(plan.end_date).toLocaleDateString()}</p>
            <div>
              <strong>Exercises:</strong>
              <ul>
                {plan.exercises.map((ex, i) => (
                  <li key={i}>{ex.name} - {ex.sets}x{ex.reps}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Plans;
