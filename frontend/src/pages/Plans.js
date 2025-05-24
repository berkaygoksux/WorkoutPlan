import React, { useState, useEffect } from 'react';
import './Plans.css';

const Plans = () => {
  const [plans, setPlans] = useState([]);

useEffect(() => {
  setPlans([
    { id: 1, title: 'Leg Day Blast', description: 'Squats, Lunges, Deadlifts' },
    { id: 2, title: 'Upper Body Pump', description: 'Push-ups, Bench Press, Pull-ups' },
    { id: 3, title: 'Core Focus', description: 'Plank, Crunches, Russian Twists' },
    { id: 4, title: 'Full Body HIIT', description: 'Burpees, Jumping Jacks, Sprints' },
    { id: 5, title: 'Cardio Burn', description: 'Treadmill, Cycling, Rowing' },
    { id: 6, title: 'Stretch & Mobility', description: 'Hamstring Stretch, Hip Opener, Shoulder Rolls' },
    { id: 7, title: 'Pilates Strength', description: 'Leg Circles, Roll Ups, Spine Stretch' },
    { id: 8, title: 'Yoga Flow', description: 'Downward Dog, Warrior, Child Pose' },
    { id: 9, title: 'Boxing Drills', description: 'Jab-Cross, Hooks, Footwork' }
  ]);
}, []);


  return (
    <div className="plans-wrapper">
      <h1>All Workout Plans</h1>
      <div className="plans-grid">
        {plans.map(plan => (
          <div key={plan.id} className="plan-card">
            <h3>{plan.title}</h3>
            <p>{plan.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Plans;
