# Deployment Guide

## Prerequisites

1. **Elastic Cloud Account**
   - Sign up at cloud.elastic.co
   - Create a deployment
   - Note your Cloud ID and credentials

2. **Google Cloud Project**
   - Create project at console.cloud.google.com
   - Enable Vertex AI API
   - Create service account with AI Platform User role
   - Download service account JSON

## Local Setup

1. **Clone and install dependencies**
   ```bash
   git clone <your-repo>
   cd smart-support-agent
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Setup data**
   ```bash
   python main.py setup
   ```

4. **Run locally**
   ```bash
   python main.py run
   ```

## Cloud Deployment

### Google Cloud Run

1. **Build and deploy**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/support-agent
   gcloud run deploy support-agent \
     --image gcr.io/YOUR_PROJECT/support-agent \
     --platform managed \
     --allow-unauthenticated
   ```

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py", "run"]
```

## Environment Variables

Required for production:
- `ELASTIC_CLOUD_ID`
- `ELASTIC_PASSWORD`
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_APPLICATION_CREDENTIALS`