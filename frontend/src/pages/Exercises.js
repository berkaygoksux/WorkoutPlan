import React, { useEffect, useState } from 'react';
import './Exercises.css';

const Exercises = () => {
  const [exercises, setExercises] = useState([]);

  useEffect(() => {
    setExercises([
      { id: 1, name: 'Push-Up', description: 'Upper body strength exercise', type: 'Bodyweight' },
      { id: 2, name: 'Squat', description: 'Leg and glute strength', type: 'Bodyweight' },
      { id: 3, name: 'Deadlift', description: 'Back, legs, and core strength', type: 'Weightlifting' },
      { id: 4, name: 'Plank', description: 'Core stability and endurance', type: 'Bodyweight' },
      { id: 5, name: 'Cycling', description: 'Cardio and leg strength', type: 'Cardio' },
      { id: 6, name: 'Burpees', description: 'Full body explosive movement', type: 'HIIT' }
    ]);
  }, []);

  return (
    <div className="exercise-wrapper">
      <h1>Discover Exercises</h1>
      <div className="exercise-grid">
        {exercises.map((ex) => (
          <div key={ex.id} className="exercise-card">
            <h3>{ex.name}</h3>
            <p>{ex.description}</p>
            <span className="exercise-type">{ex.type}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Exercises;
