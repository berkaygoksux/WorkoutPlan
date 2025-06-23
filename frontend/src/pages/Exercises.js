import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Exercises.css';

const Exercises = ({ userRole, setIsAuthenticated, setUserRole }) => {
  const [exercises, setExercises] = useState([]);
  const [error, setError] = useState('');
  const [newExercise, setNewExercise] = useState({
    name: '',
    description: '',
    muscle_group: '',
    exercise_type: 'strength',
  });
  const [editingExercise, setEditingExercise] = useState(null);
  const token = localStorage.getItem('access_token');
  const navigate = useNavigate();

  useEffect(() => {
    console.log('Exercises.js - userRole:', userRole); // userRole'ü kontrol et
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
          setExercises(data);
        } else {
          setError('Failed to fetch exercises.');
        }
      } catch (err) {
        setError('Unable to connect to the server.');
      }
    };
    fetchExercises();
  }, [token, setIsAuthenticated, setUserRole, navigate, userRole]);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/exercises`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newExercise),
      });

      if (response.status === 401) {
        localStorage.removeItem('access_token');
        setIsAuthenticated(false);
        setUserRole(null);
        navigate('/login', { replace: true });
        return;
      }

      if (response.ok) {
        const created = await response.json();
        setExercises([...exercises, created]);
        setNewExercise({ name: '', description: '', muscle_group: '', exercise_type: 'strength' });
        setError('');
        alert('Exercise created successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to create exercise: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError('Unable to connect to the server.');
    }
  };

  const handleEdit = (exercise) => {
    setEditingExercise(exercise);
    setNewExercise({
      name: exercise.name,
      description: exercise.description,
      muscle_group: exercise.muscle_group,
      exercise_type: exercise.exercise_type,
    });
    setError('');
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/exercises/${editingExercise.exercise_id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newExercise),
      });

      if (response.status === 401) {
        localStorage.removeItem('access_token');
        setIsAuthenticated(false);
        setUserRole(null);
        navigate('/login', { replace: true });
        return;
      }

      if (response.ok) {
        const updated = await response.json();
        setExercises(exercises.map((ex) => (ex.exercise_id === updated.exercise_id ? updated : ex)));
        setEditingExercise(null);
        setNewExercise({ name: '', description: '', muscle_group: '', exercise_type: 'strength' });
        setError('');
        alert('Exercise updated successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to update exercise: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError('Unable to connect to the server.');
    }
  };

  const handleDelete = async (exerciseId) => {
    if (!window.confirm('Are you sure you want to delete this exercise?')) return;
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/exercises/${exerciseId}`, {
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
        setExercises(exercises.filter((ex) => ex.exercise_id !== exerciseId));
        setError('');
        alert('Exercise deleted successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to delete exercise: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError('Unable to connect to the server.');
    }
  };

  return (
    <div className="exercise-wrapper">
      <h1>Discover Exercises</h1>
      {error && <p className="error">{error}</p>}
      {userRole === 'trainer' && (
        <div className="create-exercise">
          <h2>{editingExercise ? 'Edit Exercise' : 'Create New Exercise'}</h2>
          <form onSubmit={editingExercise ? handleUpdate : handleCreate}>
            <input
              type="text"
              placeholder="Exercise Name"
              value={newExercise.name}
              onChange={(e) => setNewExercise({ ...newExercise, name: e.target.value })}
              required
            />
            <textarea
              placeholder="Description"
              value={newExercise.description}
              onChange={(e) => setNewExercise({ ...newExercise, description: e.target.value })}
              required
            />
            <input
              type="text"
              placeholder="Muscle Group"
              value={newExercise.muscle_group}
              onChange={(e) => setNewExercise({ ...newExercise, muscle_group: e.target.value })}
              required
            />
            <select
              value={newExercise.exercise_type}
              onChange={(e) => setNewExercise({ ...newExercise, exercise_type: e.target.value })}
            >
              <option value="strength">Strength</option>
              <option value="cardio">Cardio</option>
              <option value="flexibility">Flexibility</option>
            </select>
            <button type="submit">{editingExercise ? 'Update' : 'Create'}</button>
            {editingExercise && (
              <button
                type="button"
                onClick={() => {
                  setEditingExercise(null);
                  setNewExercise({ name: '', description: '', muscle_group: '', exercise_type: 'strength' });
                  setError('');
                }}
              >
                Cancel
              </button>
            )}
          </form>
        </div>
      )}
      <div className="exercise-grid">
        {exercises.map((ex) => (
          <div key={ex.exercise_id} className="exercise-card">
            <h3>{ex.name}</h3>
            <p>{ex.description}</p>
            <p><strong>Muscle Group:</strong> {ex.muscle_group}</p>
            <span className="exercise-type">{ex.exercise_type}</span>
            {userRole === 'trainer' && (
              <div className="exercise-actions">
                <button onClick={() => handleEdit(ex)}>Edit</button>
                <button onClick={() => handleDelete(ex.exercise_id)}>Delete</button>
              </div>
            )}
          </div>
        ))}
      </div>
      <button className="back-button" onClick={() => navigate('/')}>
        Back to Home
      </button>
    </div>
  );
};

export default Exercises;