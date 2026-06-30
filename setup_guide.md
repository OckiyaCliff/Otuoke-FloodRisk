# Otuoke FloodWatch Setup Guide

A complete, step-by-step guide to setting up and running the Otuoke FloodWatch v2.0 early warning system locally.

---

## 🛠️ Step 1: Spin Up Infrastructure (Docker)
The system relies on **PostgreSQL 16** (relational database) and **Redis 7** (broker for background workers). Start them using Docker Compose:

1. Open your terminal in the root directory: `/home/ockiya-cliff/Documents/project/floodrisk`
2. Start the services in detached mode:
   ```bash
   docker compose up -d
   ```
3. Verify they are running:
   ```bash
   docker compose ps
   ```

---

## 🐍 Step 2: Backend Setup (FastAPI & Celery)
Navigate to the `backend/` directory and configure the environment:

1. Change directory to backend:
   ```bash
   cd backend
   ```
2. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install the dependencies (if not already done):
   ```bash
   pip install -r requirements.txt
   ```
4. Verify your `.env` configuration file exists. It should point to your PostgreSQL database and Redis server:
   ```env
   DATABASE_URL=postgresql+asyncpg://floodrisk:floodrisk_dev@localhost:5432/floodrisk
   REDIS_URL=redis://localhost:6379/0
   APP_ENV=development
   ```

---

## 🗄️ Step 3: Initialize Database & Train ML Model

1. **Initialize Database Schema**:
   Run the table creation script to create the necessary tables (`weather_data`, `predictions`, `alerts`, `users`):
   ```bash
   python init_db.py
   ```
2. **Train the ML Prediction Model**:
   You must train the model once so that the backend has a valid model binary (`latest_model.joblib`) to run predictions:
   ```bash
   python -m app.ml.train
   ```

---

## 🚀 Step 4: Run the Backend Services
To run the backend, you will need **three terminal windows** (with your virtual environment activated in each):

### Terminal 1: FastAPI Web Server
Start the REST API server:
```bash
uvicorn app.main:app --reload --port 8000
```
*Verify by opening your browser to [http://localhost:8000/api/health](http://localhost:8000/api/health).*

### Terminal 2: Celery Background Worker
Start the worker process that runs ML inference and dispatches notifications:
```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

### Terminal 3: Celery Beat Scheduler
Start the periodic task scheduler that triggers weather data fetching every 10 minutes:
```bash
celery -A app.tasks.celery_app beat --loglevel=info
```

---

## 💻 Step 5: Frontend Setup (SvelteKit)
Open a new terminal window in the root directory:

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node.js packages:
   ```bash
   npm install
   ```
3. Copy the environment variables example:
   ```bash
   cp .env.example .env
   ```
4. Start the SvelteKit development server:
   ```bash
   npm run dev
   ```
5. Open your browser and go to: **[http://localhost:5173](http://localhost:5173)**
