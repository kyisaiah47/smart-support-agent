"""
FastAPI main application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
from .support_agent import SupportAgent

app = FastAPI(
    title="Smart Customer Support Agent",
    description="AI-powered customer support using Elastic Search + Google Cloud AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize support agent
support_agent = SupportAgent()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    confidence: float
    intent: Dict[str, Any]
    suggested_actions: List[str]
    escalate: bool
    follow_up_questions: List[str]
    sources: List[Dict[str, str]]
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    message: str

# API Routes
@app.get("/", response_class=FileResponse)
async def read_root():
    """Serve the main chat interface"""
    return FileResponse("frontend/index.html")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test basic functionality
        test_response = support_agent.process_query(
            "test health check",
            session_id="health_check"
        )
        return HealthResponse(
            status="healthy",
            message="Support agent is operational"
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        response = support_agent.process_query(
            user_query=request.message,
            session_id=request.session_id,
            user_context=request.user_context
        )

        return ChatResponse(**response)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@app.get("/suggestions")
async def get_suggestions():
    """Get suggested questions"""
    return {
        "suggestions": support_agent.get_suggested_questions()
    }

@app.get("/conversation/{session_id}")
async def get_conversation(session_id: str):
    """Get conversation history for a session"""
    history = support_agent.get_conversation_history(session_id)
    return {
        "session_id": session_id,
        "conversation_history": history
    }

@app.get("/analytics")
async def get_analytics():
    """Get conversation analytics"""
    return support_agent.analyze_conversation_trends()

@app.get("/demo")
async def demo_scenarios():
    """Get demo scenarios for testing"""
    return {
        "demo_scenarios": [
            {
                "title": "Password Reset",
                "query": "I can't log into my account, I think I need to reset my password",
                "expected_category": "account"
            },
            {
                "title": "Billing Issue",
                "query": "Why was I charged twice this month? I only have one subscription",
                "expected_category": "billing"
            },
            {
                "title": "Integration Problem",
                "query": "My Slack integration stopped working, notifications aren't coming through",
                "expected_category": "integrations"
            },
            {
                "title": "Performance Issue",
                "query": "The dashboard is really slow, taking forever to load my projects",
                "expected_category": "technical"
            },
            {
                "title": "Team Management",
                "query": "How do I give my team member access to edit our shared project?",
                "expected_category": "team_management"
            }
        ]
    }

# Serve static files for frontend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    from ..config import Config

    print("Starting Smart Customer Support Agent...")
    print(f"Server will be available at: http://{Config.API_HOST}:{Config.API_PORT}")

    uvicorn.run(
        "src.api.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=True
    )