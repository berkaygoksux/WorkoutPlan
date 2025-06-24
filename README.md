# GymGuider Project

## Overview

GymGuider is a web application that allows both trainers and users to manage and track workout plans. The system uses role-based access: trainers can create and assign workout plans and logs; users can view and manage their own plans and logs. The app is designed for efficient and structured fitness planning.


## Project Structure

```
WorkoutPlan/
├── app/
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── workout_controller.py
│   │   └── workout_log_controller.py
│   ├── models/
│   │   ├── exercise.py
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── workout_log.py
│   │   └── workout_plan.py
│   ├── patterns/
│   │   ├── api_facade.py
│   │   ├── observers.py
│   │   └── workout_commands.py
│   ├── services/
│   │   └── workout_plan_service.py
│   ├── database.py
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   │   └── (React pages)
│   │   ├── App.js
│   │   ├── index.js
│   │   └── ...
│   └── .env
├── gymguidervenv/
├── gymguider.db
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Technologies Used

- **Frontend**: React.js, fetch API, React Router, localStorage
- **Backend**: FastAPI, SQLAlchemy, Pydantic, JWT, SQLite
- **Auth**: JWT-based authentication with access tokens
- **Database**: SQLite (gymguider.db)

## Setup Instructions

### Backend

1. Create and activate the virtual environment:
    ```bash
    python -m venv gymguidervenv
    source gymguidervenv/bin/activate  # For Linux/macOS
    # OR
    .\gymguidervenv\Scripts\activate  # For Windows
    ```

2. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

3. Create `.env` in the root directory:
    ```
    SECRET_KEY=your-secret-key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=sqlite:///gymguider.db
    ```

4. Run the backend server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1. Go to the frontend folder:
    ```bash
    cd frontend
    ```

2. Create `.env`:
    ```
    REACT_APP_API_URL=http://127.0.0.1:8000
    ```

3. Install dependencies:
    ```bash
    npm install
    ```

4. Start the frontend:
    ```bash
    npm start
    ```

## Roles & Features

### User
- Register and login
- Create/view their own workout plans
- Add workout logs

### Trainer
- Register and login
- Create/view plans for any user
- View all logs and assign plans
- Acts like an admin in functionality

## Authentication

- JWT tokens are issued on login and stored in `localStorage`
- Used in headers: `Authorization: Bearer <token>`
- Token payload includes `sub` (email) and `role`

## API Highlights

- `POST /auth/register`
- `POST /auth/login`
- `GET /user/me`
- `GET/POST /workout/plans`
- `GET /workout/exercises`

## Database Tables

- `users`: user_id, name, email, password_hash, role
- `workout_plans`: plan_id, user_id (FK), title, level, exercises (JSON), start_date, end_date
- `exercises`: name, description, type, muscle group
- `workout_logs`: log_id, user_id, exercise_id, date, sets, reps, duration, notes

## Developer Notes

- API docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Trainer can view which user a plan belongs to
- Clean modular code with Facade and Observer patterns
