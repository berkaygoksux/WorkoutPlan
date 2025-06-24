import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './CreatePlan.css';

const CreatePlan = ({ userRole, setIsAuthenticated, setUserRole }) => {
  const [form, setForm] = useState({
    title: '',
    level: '',
    start_date: '',
    end_date: '',
    exercises: [],
    user_id: '',
  });
  const [availableExercises, setAvailableExercises] = useState([]);
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');

  useEffect(() => {
    if (!token) {
      setIsAuthenticated(false);
      setUserRole(null);
      navigate('/login', { replace: true });
      return;
    }

    const fetchExercises = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/exercises`, {
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
          setAvailableExercises(data);
        } else {
          setError('Failed to fetch exercises.');
        }
      } catch (err) {
        setError(`Network error: ${err.message || 'Failed to fetch exercises.'}`);
      }
    };

    const fetchUsers = async () => {
      if (userRole !== 'trainer') return;
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/user`, {
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
          setUsers(data);
        } else {
          setError('Failed to fetch users.');
        }
      } catch (err) {
        setError(`Network error: ${err.message || 'Failed to fetch users.'}`);
      }
    };

    fetchExercises();
    fetchUsers();
  }, [token, userRole, setIsAuthenticated, setUserRole, navigate]);

  const handleAddExercise = (exerciseId) => {
    const exercise = availableExercises.find((ex) => ex.exercise_id === parseInt(exerciseId));
    if (exercise && !form.exercises.find((ex) => ex.exercise_id === exercise.exercise_id)) {
      setForm({
        ...form,
        exercises: [
          ...form.exercises,
          {
            exercise_id: exercise.exercise_id,
            name: exercise.name,
            sets: 3,
            reps: 10,
            rest_seconds: 30,
          },
        ],
      });
    } else if (exercise) {
      alert('This exercise is already added.');
    }
  };

  const handleRemoveExercise = (exerciseId) => {
    setForm({
      ...form,
      exercises: form.exercises.filter((ex) => ex.exercise_id !== exerciseId),
    });
  };

  const handleExerciseChange = (index, field, value) => {
    const updatedExercises = [...form.exercises];
    updatedExercises[index] = {
      ...updatedExercises[index],
      [field]: field === 'name' ? value : parseInt(value) || 0,
    };
    setForm({ ...form, exercises: updatedExercises });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.exercises.length === 0) {
      setError('Please add at least one exercise.');
      return;
    }
    setLoading(true);
    try {
      const payload = {
        title: form.title,
        level: form.level,
        start_date: form.start_date,
        end_date: form.end_date,
        exercises: form.exercises.map((ex) => ({
          exercise_id: ex.exercise_id,
          sets: ex.sets,
          reps: ex.reps,
          rest_seconds: ex.rest_seconds,
        })),
        user_id: userRole === 'trainer' && form.user_id ? parseInt(form.user_id) : undefined,
      };
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/plans`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (response.status === 401) {
        localStorage.removeItem('access_token');
        setIsAuthenticated(false);
        setUserRole(null);
        navigate('/login', { replace: true });
        return;
      }
      if (response.ok) {
        setForm({
          title: '',
          level: '',
          start_date: '',
          end_date: '',
          exercises: [],
          user_id: '',
        });
        setError('');
        alert('Workout plan created successfully!');
        navigate('/plans');
      } else {
        const err = await response.json();
        setError(`Failed to create plan: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Network error: ${err.message || 'Failed to create workout plan.'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-plan-wrapper">
      <h1 className="create-plan-title">Create Workout Plan</h1>
      {error && <p className="error-message" data-testid="error-message">{error}</p>}
      {loading && <p className="loading-message" data-testid="loading-message">Loading...</p>}
      <form onSubmit={handleSubmit} className="create-plan-form">
        <input
          type="text"
          placeholder="Plan Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          required
        />
        <select
          value={form.level}
          onChange={(e) => setForm({ ...form, level: e.target.value })}
          required
        >
          <option value="" disabled>Select Level</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        <input
          type="date"
          value={form.start_date}
          onChange={(e) => setForm({ ...form, start_date: e.target.value })}
          required
        />
        <input
          type="date"
          value={form.end_date}
          onChange={(e) => setForm({ ...form, end_date: e.target.value })}
          required
        />
        {userRole === 'trainer' && (
          <select
            value={form.user_id}
            onChange={(e) => setForm({ ...form, user_id: e.target.value })}
          >
            <option value="">Select User (Optional)</option>
            {users.map((user) => (
              <option key={user.user_id} value={user.user_id}>{user.name} ({user.email})</option>
            ))}
          </select>
        )}
        <div className="exercise-selection">
          <h3>Exercises</h3>
          <select onChange={(e) => handleAddExercise(e.target.value)} value="">
            <option value="" disabled>Add Exercise</option>
            {availableExercises.map((ex) => (
              <option key={ex.exercise_id} value={ex.exercise_id}>{ex.name}</option>
            ))}
          </select>
          <ul>
            {form.exercises.map((ex, index) => (
              <li key={ex.exercise_id} className="exercise-item">
                <span>{ex.name}</span>
                <input
                  type="number"
                  placeholder="Sets"
                  value={ex.sets}
                  onChange={(e) => handleExerciseChange(index, 'sets', e.target.value)}
                  required
                />
                <input
                  type="number"
                  placeholder="Reps"
                  value={ex.reps}
                  onChange={(e) => handleExerciseChange(index, 'reps', e.target.value)}
                  required
                />
                <input
                  type="number"
                  placeholder="Rest (seconds)"
                  value={ex.rest_seconds}
                  onChange={(e) => handleExerciseChange(index, 'rest_seconds', e.target.value)}
                  required
                />
                <button
                  type="button"
                  onClick={() => handleRemoveExercise(ex.exercise_id)}
                  className="remove-exercise"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        </div>
        <div className="form-actions">
          <button type="submit" disabled={loading} className="submit-button">Create Plan</button>
          <button
            type="button"
            onClick={() => navigate('/plans')}
            disabled={loading}
            className="cancel-button"
          >
            Cancel
          </button>
        </div>
      </form>
      <button className="back-button" onClick={() => navigate('/')}>Back to Main Menu</button>
    </div>
  );
};

export default CreatePlan;