import React, { useState, useEffect } from 'react';
import './CreatePlan.css';

const CreatePlan = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [exercises, setExercises] = useState('');
  const [availableExercises, setAvailableExercises] = useState([]);
  const token = localStorage.getItem('access_token');

  useEffect(() => {
    const fetchExercises = async () => {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_URL}/workout/exercises`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();
        if (Array.isArray(data)) {
          setAvailableExercises(data);
        } else {
          setAvailableExercises([]);
        }
      } catch (err) {
        console.error('Exercise fetch error:', err);
        setAvailableExercises([]);
      }
    };
    fetchExercises();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const parsedExercises = exercises
      .split('\n')
      .filter(line => line.trim() !== '')
      .map((name, index) => {
        const match = availableExercises.find(ex => ex.name.toLowerCase() === name.toLowerCase().trim());
        return match ? {
          exercise_id: match.exercise_id,
          name: match.name,
          description: match.description,
          sets: 3,
          reps: 10
        } : null;
      })
      .filter(ex => ex !== null);

    const payload = {
      title,
      level: 'Beginner',
      start_date: new Date().toISOString().split('T')[0],
      end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      exercises: parsedExercises
    };

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/workout/plans`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        alert('Exercise Plan Created');
        } else {
        const err = await res.json();
        const errorMsg = err.detail || JSON.stringify(err);
        alert(`Failed to create plan: ${errorMsg}`);
        }
    } catch (err) {
      console.error('Submit error:', err);
      alert('Something went wrong.');
    }
  };

  return (
    <div className="create-plan-wrapper">
      <h1>Create New Workout Plan</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Plan Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <textarea
          placeholder="Exercises (one per line)"
          value={exercises}
          onChange={(e) => setExercises(e.target.value)}
        />
        <button type="submit">Save Plan</button>

        <h2 className="section-title">Example Classes</h2>
        <div className="class-gallery">
          <div className="class-item">
            <img src="/images/cardio.png" alt="Cardio" />
            <p>Cardio</p>
          </div>
          <div className="class-item">
            <img src="/images/cycling.png" alt="Cycling" />
            <p>Cycling</p>
          </div>
          <div className="class-item">
            <img src="/images/yoga.png" alt="Yoga" />
            <p>Yoga</p>
          </div>
          <div className="class-item">
            <img src="/images/pilates.png" alt="Pilates" />
            <p>Pilates</p>
          </div>
        </div>
      </form>
    </div>
  );
};

export default CreatePlan;
