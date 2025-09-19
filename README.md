# Smart Customer Support Agent

AI-powered customer support agent using Elastic Search + Google Cloud AI for the AI Accelerate Hackathon.

## Architecture
- **Search**: Elastic Cloud with hybrid search (keyword + vector)
- **AI**: Google Cloud Vertex AI (Gemini Pro)
- **Backend**: Python FastAPI
- **Frontend**: React chat interface
- **Data**: Sample CloudFlow SaaS support knowledge base

## Setup
1. Configure Elastic Cloud
2. Set up Google Cloud project
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`

## Demo
Chat interface that handles customer queries by searching knowledge base and generating contextual responses.