# FraudShield: Credit Card Fraud Detection API

A production-ready FastAPI application for predicting credit card fraud. This project was refactored into a scalable MLOps pipeline with structured architecture, batch prediction, SQLite history, and deployment-ready files.

## Architecture & Features

- **Clean FastAPI Architecture**: Separated into `api`, `core`, `ml`, `schemas`, and `services`.
- **Pydantic Validation**: Strong request/response schemas for robustness.
- **Model Metadata**: Inspect model version and type.
- **Batch Processing**: Upload CSV files for large-scale fraud detection.
- **Prediction History**: Local SQLite database logging predictions.
- **Health Checks**: `/api/v1/health` endpoint for monitoring.
- **Rate Limiting**: Protects against abusive requests.
- **Docker Ready**: Pre-configured `Dockerfile` and `render.yaml`.

## Project Structure

```text
.
├── app/
│   ├── api/          # API Routers and endpoints
│   ├── core/         # Settings, logging, config
│   ├── db/           # Database sessions and models
│   ├── ml/           # Model loading and abstraction
│   ├── schemas/      # Pydantic models for validation
│   └── services/     # Core prediction business logic
├── data/             # SQLite storage
├── .env.example      # Environment variable template
├── Dockerfile        # Docker container configuration
├── Procfile          # Render / Railway startup command
├── render.yaml       # Render.com deployment script
├── requirements.txt  # Python dependencies
└── main.py           # Application entrypoint
```

## Running Locally

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

3. Start the application:
   ```bash
   uvicorn main:app --reload
   ```

4. View API Documentation:
   Navigate to `http://localhost:8000/docs` (Swagger UI).

## Deployment

### Render Deployment
This repository is configured for easy deployment on [Render](https://render.com).
1. Push this code to GitHub.
2. In Render, select **New -> Blueprint**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml` and deploy your API as a Docker service.

## Endpoints

- `GET /` - Root message
- `GET /api/v1/health` - Health check status
- `GET /api/v1/model-info` - Deployed model metadata
- `POST /api/v1/predict/` - Predict fraud for a single transaction
- `POST /api/v1/predict/batch` - Batch prediction via CSV file upload

## Example Request (Single Prediction)

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Time": 0,
  "V1": -1.3598,
  "V2": -0.0727,
  "V3": 2.5363,
  "V4": 1.3781,
  "V5": -0.3383,
  "V6": 0.4623,
  "V7": 0.2395,
  "V8": 0.0986,
  "V9": 0.3637,
  "V10": 0.0907,
  "V11": -0.5516,
  "V12": -0.6178,
  "V13": -0.9913,
  "V14": -0.3111,
  "V15": 1.4681,
  "V16": -0.4704,
  "V17": 0.2079,
  "V18": 0.0257,
  "V19": 0.4039,
  "V20": 0.2514,
  "V21": -0.0183,
  "V22": 0.2778,
  "V23": -0.1104,
  "V24": 0.0669,
  "V25": 0.1285,
  "V26": -0.1891,
  "V27": 0.1335,
  "V28": -0.0210,
  "Amount": 149.62
}'
```
