# ThermaGuard AI - Predictive Cold-Chain Monitoring System

A production-ready AI system for real-time temperature monitoring, anomaly detection, and predictive alerts in cold-chain logistics.

## 🎯 Overview

ThermaGuard AI ingests time-series temperature sensor data, uses Prophet for forecasting, detects anomalies 4+ hours before failure, and sends proactive alerts via SMS.

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Sensors    │───▶│  InfluxDB   │───▶│  Prophet    │
│  (Time-series)│   │  (Storage)  │    │  (Forecast) │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FastAPI   │◀───│  Anomaly    │───▶│   Twilio    │
│  (REST API) │    │  Detection  │    │  (Alerts)   │
└─────────────┘    └─────────────┘    └─────────────┘
       ▲
       │
┌─────────────┐
│   Celery    │
│  (Scheduler)│
└─────────────┘
```

## 🚀 Features

- **Real-time Ingestion**: 1-minute interval temperature data processing
- **Prophet Forecasting**: 6-hour ahead temperature predictions
- **Early Anomaly Detection**: Threshold breaches detected 4+ hours early
- **Proactive Alerts**: SMS notifications via Twilio
- **RESTful API**: FastAPI with async support
- **Scalable Architecture**: Celery for background tasks
- **Production Ready**: Docker, logging, monitoring

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/Anusha0501/ThermaGuard-AI.git
cd ThermaGuard-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

## 🔧 Configuration

Edit `.env` file with your settings:
- InfluxDB connection details
- Redis for Celery
- Twilio credentials for SMS alerts
- Temperature thresholds

## 🏃 Running

```bash
# Start API server
uvicorn thermaguard.api.main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker (in separate terminal)
celery -A thermaguard.tasks.celery_app worker --loglevel=info

# Start Celery beat scheduler (in separate terminal)
celery -A thermaguard.tasks.celery_app beat --loglevel=info
```

## 📡 API Endpoints

- `POST /ingest` - Ingest temperature sensor data
- `GET /forecast/{chamber}` - Get 6-hour forecast for a chamber
- `GET /alerts` - Get recent alerts
- `GET /status/{chamber}` - Get chamber status
- `GET /health` - Health check

## 🐳 Docker

```bash
# Build image
docker build -t thermaguard-ai .

# Run container
docker run -p 8000:8000 --env-file .env thermaguard-ai
```

## 📊 Performance

- **Processing Time**: <50ms per chamber
- **Forecast Horizon**: 6 hours
- **Detection Window**: 4+ hours before failure
- **Data Resolution**: 1-minute intervals

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=thermaguard --cov-report=html
```

## 📈 Monitoring

- Prometheus metrics exposed at `/metrics`
- Structured logging with Loguru
- Health check endpoint

## 🔐 Security

- Environment-based configuration
- No hardcoded credentials
- Input validation with Pydantic
- Rate limiting ready

## 📝 License

MIT License - see LICENSE file

## 👤 Author

Built by Anusha - Senior Python Backend & ML Engineer

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md
