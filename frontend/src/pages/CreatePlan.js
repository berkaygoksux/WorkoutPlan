import React, { useState } from 'react';
import './CreatePlan.css';

const CreatePlan = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [exercises, setExercises] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Yeni Plan:', {
      title,
      description,
      exercises: exercises.split('\n'), // her satır bir egzersiz
    });
    alert('Plan oluşturuldu! (Henüz backend bağlı değil)');
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
