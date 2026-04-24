# Otuoke FloodWatch 🌊

Production-ready flood early-warning platform for Federal University Otuoke.

## Architecture

- **Backend**: FastAPI (Python 3.12)
- **Frontend**: SvelteKit (TypeScript)
- **ML Engine**: Random Forest Classifier (Scikit-Learn)
- **Background Tasks**: Celery + Redis
- **Database**: PostgreSQL
- **Notifications**: SuprSend (Multi-channel: SMS, Email, Push)

## System Flow

1. **Data Ingestion**: Periodic tasks fetch environmental data (rainfall, river levels).
2. **ML Inference**: Data is preprocessed and passed to the Random Forest model to predict flood risk.
3. **Alert Trigger**: If risk level exceeds thresholds, an alert event is generated.
4. **Notification**: SuprSend dispatches alerts across configured channels to registered users.
5. **Monitoring**: Real-time dashboard visualizes current risk and historical trends.

## Setup & Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Node.js 18+

### Running Locally
1. Start infrastructure: `docker-compose up -d`
2. Backend setup:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
3. Frontend setup:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Deployment

- **Backend**: Configured for **Render** via `render.yaml`.
- **Frontend**: Configured for **Vercel** via `vercel.json`.
