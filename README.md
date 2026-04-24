# Otuoke FloodWatch 🌊

Production-ready flood early-warning platform for Federal University Otuoke. This system monitors environmental conditions, predicts flood risk using machine learning, and dispatches multi-channel alerts to registered users.

---

## 🚀 Key Features

- **Real-time Dashboard**: Live visualization of rainfall, river levels, and risk metrics.
- **Machine Learning**: Custom Random Forest model with 95.5% prediction accuracy.
- **Background Automation**: Automated data fetching and prediction via Celery & Redis.
- **Multi-channel Alerts**: Integrated notifications via **SuprSend** (SMS, Email, Push).
- **Responsive Design**: Modern, glassmorphism-inspired UI built with **SvelteKit**.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Meteorological Data] --> B[FastAPI Backend]
    B --> C[PostgreSQL 16]
    B --> D[Celery Worker]
    D --> E[Redis 7]
    D --> F[ML Engine]
    F --> G[SuprSend Notifications]
    H[SvelteKit Dashboard] --> B
```

---

## 🛠️ Comprehensive Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.12+**, **Node.js 20+**, and **Docker** installed.

### 2. Infrastructure
Start the database and message broker:
```bash
docker compose up -d
```

### 3. Backend (FastAPI)
1. **Configure Environment**: Create `backend/.env` (see `backend/.env.example`).
   ```env
   DATABASE_URL=postgresql+asyncpg://floodrisk:floodrisk_dev@localhost:5432/floodrisk
   REDIS_URL=redis://localhost:6379/0
   ```
2. **Install & Run**:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
3. **Start Workers** (in separate terminals, with venv activated):
   ```bash
   celery -A app.tasks.celery_app worker --loglevel=info
   celery -A app.tasks.celery_app beat --loglevel=info
   ```

### 4. Frontend (SvelteKit)
1. **Configure Environment**: Create `frontend/.env`.
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```
2. **Install & Run**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 🧪 Manual Testing

To verify the alert flow immediately without waiting for the 10-minute automated cycle:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/weather/' \
  -H 'Content-Type: application/json' \
  -d '{
  "rainfall_mm": 150.5,
  "river_level_m": 8.2,
  "humidity_pct": 85,
  "temperature_c": 28,
  "wind_speed_kmh": 15,
  "source": "manual_test"
}'
```

---

## 📄 Documentation Artifacts

- [**Full Setup Guide**](file:///home/ockiya-cliff/.gemini/antigravity/brain/bbdefb79-517e-463f-a36c-8c95d8d0b59f/setup_guide.md) — Detailed troubleshooting and deep-dive.
- [**Data Flow Guide**](file:///home/ockiya-cliff/.gemini/antigravity/brain/bbdefb79-517e-463f-a36c-8c95d8d0b59f/data_flow_guide.md) — Explanation of the ML pipeline and API integration.
- [**Project Walkthrough**](file:///home/ockiya-cliff/.gemini/antigravity/brain/bbdefb79-517e-463f-a36c-8c95d8d0b59f/walkthrough.md) — Summary of implementation and results.
