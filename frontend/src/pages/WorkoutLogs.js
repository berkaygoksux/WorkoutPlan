import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './WorkoutLogs.css';

const WorkoutLogs = ({ userRole, setIsAuthenticated, setUserRole }) => {
  const [logs, setLogs] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [newLog, setNewLog] = useState({
    exercise_id: '',
    sets: 3,
    reps: 10,
    date: new Date().toISOString().split('T')[0],
    duration: 30,
    notes: '',
  });
  const [editingLog, setEditingLog] = useState(null);
  const [exercises, setExercises] = useState([]);
  const token = localStorage.getItem('access_token');
  const navigate = useNavigate();

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

    const fetchLogs = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/logs`, {
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
          setLogs(data);
          setError('');
        } else {
          const err = await response.json();
          setError(`Failed to fetch workout logs: ${err.detail || 'Unknown error'}`);
        }
      } catch (err) {
        setError(`Network error: ${err.message || 'Failed to fetch workout logs.'}`);
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
          setExercises(data);
        } else {
          setError('Failed to fetch exercises.');
        }
      } catch (err) {
        setError(`Network error: ${err.message || 'Failed to fetch exercises.'}`);
      }
    };

    fetchCurrentUser();
    fetchLogs();
    fetchExercises();
  }, [token, setIsAuthenticated, setUserRole, navigate]);

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const selectedExercise = exercises.find((ex) => ex.exercise_id === parseInt(newLog.exercise_id));
      if (!selectedExercise) {
        setError('Please select a valid exercise.');
        setLoading(false);
        return;
      }
      const payload = {
        exercise_id: parseInt(newLog.exercise_id),
        exercise_name: selectedExercise.name,
        exercise_description: selectedExercise.description || '',
        sets: parseInt(newLog.sets),
        reps: parseInt(newLog.reps),
        date: newLog.date,
        duration: parseInt(newLog.duration),
        notes: newLog.notes,
      };
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/logs`, {
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
        const newLogData = await response.json();
        setLogs([...logs, newLogData]);
        setNewLog({
          exercise_id: '',
          sets: 3,
          reps: 10,
          date: new Date().toISOString().split('T')[0],
          duration: 30,
          notes: '',
        });
        setError('');
        alert('Workout log created successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to create log: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Network error: ${err.message || 'Failed to create workout log.'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (log) => {
    setEditingLog(log);
    setNewLog({
      exercise_id: log.exercise_id.toString(),
      sets: log.sets,
      reps: log.reps,
      date: log.date.split('T')[0],
      duration: log.duration,
      notes: log.notes || '',
    });
    setError('');
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const selectedExercise = exercises.find((ex) => ex.exercise_id === parseInt(newLog.exercise_id));
      if (!selectedExercise) {
        setError('Please select a valid exercise.');
        setLoading(false);
        return;
      }
      const payload = {
        exercise_id: parseInt(newLog.exercise_id),
        exercise_name: selectedExercise.name,
        exercise_description: selectedExercise.description || '',
        sets: parseInt(newLog.sets),
        reps: parseInt(newLog.reps),
        date: newLog.date,
        duration: parseInt(newLog.duration),
        notes: newLog.notes,
      };
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/logs/${editingLog.log_id}`, {
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
        const updatedLog = await response.json();
        setLogs(logs.map((log) => (log.log_id === updatedLog.log_id ? updatedLog : log)));
        setEditingLog(null);
        setNewLog({
          exercise_id: '',
          sets: 3,
          reps: 10,
          date: new Date().toISOString().split('T')[0],
          duration: 30,
          notes: '',
        });
        setError('');
        alert('Workout log updated successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to update log: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Network error: ${err.message || 'Failed to update workout log.'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (logId) => {
    if (!window.confirm('Are you sure you want to delete this workout log?')) return;
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/workout/logs/${logId}`, {
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
        setLogs(logs.filter((log) => log.log_id !== logId));
        setError('');
        alert('Workout log deleted successfully!');
      } else {
        const err = await response.json();
        setError(`Failed to delete log: ${err.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Network error: ${err.message || 'Failed to delete workout log.'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="logs-wrapper">
      <h1 className="logs-title">{userRole === 'trainer' ? 'All Workout Logs' : 'Your Workout Logs'}</h1>
      {error && <p className="error-message" data-testid="error-message">{error}</p>}
      {loading && <p className="loading-message" data-testid="loading-message">Loading...</p>}

      <div className="log-form">
        <h2>{editingLog ? 'Edit Workout Log' : 'Create Workout Log'}</h2>
        <form onSubmit={editingLog ? handleUpdate : handleCreate}>
          <select
            value={newLog.exercise_id}
            onChange={(e) => setNewLog({ ...newLog, exercise_id: e.target.value })}
            required
          >
            <option value="" disabled>Select Exercise</option>
            {exercises.map((ex) => (
              <option key={ex.exercise_id} value={ex.exercise_id}>{ex.name}</option>
            ))}
          </select>
          <input
            type="number"
            placeholder="Sets"
            value={newLog.sets}
            onChange={(e) => setNewLog({ ...newLog, sets: parseInt(e.target.value) || '' })}
            required
          />
          <input
            type="number"
            placeholder="Reps"
            value={newLog.reps}
            onChange={(e) => setNewLog({ ...newLog, reps: parseInt(e.target.value) || '' })}
            required
          />
          <input
            type="date"
            value={newLog.date}
            onChange={(e) => setNewLog({ ...newLog, date: e.target.value })}
            required
          />
          <input
            type="number"
            placeholder="Duration (minutes)"
            value={newLog.duration}
            onChange={(e) => setNewLog({ ...newLog, duration: parseInt(e.target.value) || '' })}
            required
          />
          <textarea
            placeholder="Notes"
            value={newLog.notes}
            onChange={(e) => setNewLog({ ...newLog, notes: e.target.value })}
          />
          <div className="form-actions">
            <button type="submit" disabled={loading} className="submit-button">
              {editingLog ? 'Update Log' : 'Create Log'}
            </button>
            {editingLog && (
              <button
                type="button"
                onClick={() => {
                  setEditingLog(null);
                  setNewLog({
                    exercise_id: '',
                    sets: 3,
                    reps: 10,
                    date: new Date().toISOString().split('T')[0],
                    duration: 30,
                    notes: '',
                  });
                  setError('');
                }}
                disabled={loading}
                className="cancel-button"
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="logs-grid">
        {logs.length > 0 ? (
          logs.map((log) => (
            <div key={log.log_id} className="log-card">
              <h3>{log.exercise_name || 'Unknown Exercise'}</h3>
              <p><strong>Sets:</strong> {log.sets}</p>
              <p><strong>Reps:</strong> {log.reps}</p>
              <p><strong>Date:</strong> {new Date(log.date).toLocaleDateString('en-US')}</p>
              <p><strong>Duration:</strong> {log.duration} minutes</p>
              {log.notes && <p><strong>Notes:</strong> {log.notes}</p>}
              {(userRole === 'trainer' || (currentUser && log.user_id === currentUser.user_id)) && (
                <div className="log-actions">
                  <button onClick={() => handleEdit(log)} disabled={loading} className="edit-button">
                    Edit
                  </button>
                  <button onClick={() => handleDelete(log.log_id)} disabled={loading} className="delete-button">
                    Delete
                  </button>
                </div>
              )}
            </div>
          ))
        ) : (
          <p className="no-logs" data-testid="no-logs">No workout logs found.</p>
        )}
      </div>
      <button className="back-button" onClick={() => navigate('/')}>Back to Main Menu</button>
    </div>
  );
};

export default WorkoutLogs;