import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Plans.css';

const Plans = ({ userRole, setIsAuthenticated, setUserRole }) => {
  const [plans, setPlans] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);
  const [editForm, setEditForm] = useState({
    title: '',
    level: '',
    start_date: '',
    end_date: '',
    exercises: [],
  });
  const [availableExercises, setAvailableExercises] = useState([]);
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');

  useEffect(() => {
    if (!token) {
      setIsAuthenticated(false);
      setUserRole(null);
      navigate('/login', { replace: true });
      return;
    }

    const fetchCurrentUser = async () => {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_URL}/user/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.status === 401) {
          localStorage.removeItem('access_token');
          setIsAuthenticated(false);
          setUserRole(null);
          navigate('/login', { replace: true });
          return;
        }
        if (res.ok) {
          const data = await res.json();
          setCurrentUser(data);
        } else {
          setError('Failed to fetch user information.');
        }
      } catch (err) {
        setError('Unable to connect to the server.');
      }
    };

    const fetchPlans = async () => {
      setLoading(true);
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
        if (!response.ok) {
          const err = await response.json();
          throw new Error(err.detail || 'Failed to fetch workout plans.');
        }
        const data = await response.json();
        setPlans(data);
        setError('');
      } catch (err) {
        setError(`Error loading plans: ${err.message || 'Network error'}`);
      } finally {
        setLoading(false);
      }
    };

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
        setError(`Error loading exercises: ${err.message || 'Network error'}`);
      }
    };

    fetchCurrentUser();
    fetchPlans();
    fetchExercises();
  }, [navigate, token, setIsAuthenticated, setUserRole]);

  const handleDelete = async (planId) => {
    if (!window.confirm('Are you sure you want to delete this plan?')) return;
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/plans/${planId}`, {
        method: 'DELETE',
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
        setPlans(plans.filter((plan) => plan.plan_id !== planId));
        setError('');
        alert('Workout plan deleted successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to delete plan: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Failed to delete plan: ${err.message || 'Network error'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (plan) => {
    setEditingPlan(plan);
    setEditForm({
      title: plan.title,
      level: plan.level,
      start_date: plan.start_date.split('T')[0],
      end_date: plan.end_date.split('T')[0],
      exercises: plan.exercises.map((ex) => ({
        exercise_id: ex.exercise_id,
        name: ex.name || 'Unknown Exercise',
        sets: ex.sets,
        reps: ex.reps,
        rest_seconds: ex.rest_seconds || 30,
      })),
    });
    setError('');
  };

  const handleAddExercise = (exerciseId) => {
    const exercise = availableExercises.find((ex) => ex.exercise_id === parseInt(exerciseId));
    if (exercise && !editForm.exercises.find((ex) => ex.exercise_id === exercise.exercise_id)) {
      setEditForm({
        ...editForm,
        exercises: [
          ...editForm.exercises,
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
    setEditForm({
      ...editForm,
      exercises: editForm.exercises.filter((ex) => ex.exercise_id !== exerciseId),
    });
  };

  const handleExerciseChange = (index, field, value) => {
    const updatedExercises = [...editForm.exercises];
    updatedExercises[index] = {
      ...updatedExercises[index],
      [field]: field === 'name' ? value : parseInt(value) || 0,
    };
    setEditForm({ ...editForm, exercises: updatedExercises });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (editForm.exercises.length === 0) {
      setError('Please add at least one exercise.');
      return;
    }
    setLoading(true);
    try {
      const payload = {
        title: editForm.title,
        level: editForm.level,
        start_date: editForm.start_date,
        end_date: editForm.end_date,
        exercises: editForm.exercises.map((ex) => ({
          exercise_id: ex.exercise_id,
          sets: ex.sets,
          reps: ex.reps,
          rest_seconds: ex.rest_seconds,
        })),
      };
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/plans/${editingPlan.plan_id}`, {
        method: 'PUT',
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
        const updatedPlan = await response.json();
        setPlans(plans.map((p) => (p.plan_id === updatedPlan.plan_id ? updatedPlan : p)));
        setEditingPlan(null);
        setEditForm({
          title: '',
          level: '',
          start_date: '',
          end_date: '',
          exercises: [],
        });
        setError('');
        alert('Workout plan updated successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to update plan: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Failed to update plan: ${err.message || 'Network error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="plans-wrapper">
      <h1 className="plans-title">{userRole === 'trainer' ? 'All Workout Plans' : 'Your Workout Plans'}</h1>
      {error && <p className="error-message" data-testid="error-message">{error}</p>}
      {loading && <p className="loading-message" data-testid="loading-message">Loading...</p>}
      <div className="plans-grid">
        {plans.length > 0 ? (
          plans.map((plan) => (
            <div key={plan.plan_id} className="plan-card">
              <h3>
                {plan.title} <span className="owner-name">by {plan.owner_name || 'Unknown'}</span>
              </h3>
              <p><strong>Level:</strong> {plan.level}</p>
              <p><strong>Start:</strong> {new Date(plan.start_date).toLocaleDateString('en-US')}</p>
              <p><strong>End:</strong> {new Date(plan.end_date).toLocaleDateString('en-US')}</p>
              <div>
                <strong>Exercises:</strong>
                <ul>
                  {plan.exercises && plan.exercises.length > 0 ? (
                    plan.exercises.map((ex, i) => (
                      <li key={i}>
                        {ex.name || 'Unknown Exercise'} - {ex.sets}x{ex.reps} (Rest: {ex.rest_seconds || 30}s)
                      </li>
                    ))
                  ) : (
                    <li>No exercises assigned</li>
                  )}
                </ul>
              </div>
              {(userRole === 'trainer' || (currentUser && plan.user_id === currentUser.user_id)) && (
                <div className="plan-actions">
                  <button onClick={() => handleEdit(plan)} disabled={loading} className="edit-button">
                    Edit
                  </button>
                  <button onClick={() => handleDelete(plan.plan_id)} disabled={loading} className="delete-button">
                    Delete
                  </button>
                </div>
              )}
            </div>
          ))
        ) : (
          <p className="no-plans" data-testid="no-plans">No workout plans found.</p>
        )}
      </div>

      {editingPlan && (
        <div className="modal">
          <div className="modal-content">
            <h2>Edit Workout Plan</h2>
            <form onSubmit={handleUpdate}>
              <input
                type="text"
                value={editForm.title}
                onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                placeholder="Plan Title"
                required
              />
              <select
                value={editForm.level}
                onChange={(e) => setEditForm({ ...editForm, level: e.target.value })}
                required
              >
                <option value="" disabled>Select Level</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
              <input
                type="date"
                value={editForm.start_date}
                onChange={(e) => setEditForm({ ...editForm, start_date: e.target.value })}
                required
              />
              <input
                type="date"
                value={editForm.end_date}
                onChange={(e) => setEditForm({ ...editForm, end_date: e.target.value })}
                required
              />
              <div className="exercise-selection">
                <h3>Exercises</h3>
                <select onChange={(e) => handleAddExercise(e.target.value)} value="">
                  <option value="" disabled>Add Exercise</option>
                  {availableExercises.map((ex) => (
                    <option key={ex.exercise_id} value={ex.exercise_id}>{ex.name}</option>
                  ))}
                </select>
                <ul>
                  {editForm.exercises.map((ex, index) => (
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
                <button type="submit" disabled={loading} className="update-button">Update</button>
                <button
                  type="button"
                  onClick={() => {
                    setEditingPlan(null);
                    setEditForm({ title: '', level: '', start_date: '', end_date: '', exercises: [] });
                    setError('');
                  }}
                  disabled={loading}
                  className="cancel-button"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      <button className="back-button" onClick={() => navigate('/')}>Back to Main Menu</button>
    </div>
  );
};

export default Plans;