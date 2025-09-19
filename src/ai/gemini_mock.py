"""
Mock Gemini client for demo purposes
"""
import json
import random
from typing import List, Dict, Any

class GeminiClient:
    def __init__(self):
        pass

    def generate_embedding(self, text: str) -> List[float]:
        """Generate deterministic embedding for text"""
        random.seed(hash(text))
        return [random.uniform(-1, 1) for _ in range(768)]

    def analyze_intent(self, user_query: str) -> Dict[str, Any]:
        """Analyze user intent with smart responses"""
        query_lower = user_query.lower()

        if any(word in query_lower for word in ["password", "login", "access", "account"]):
            return {
                "intent": "account",
                "urgency": "high",
                "entities": ["password", "account"],
                "tone": "frustrated",
                "keywords": ["password", "reset", "login"]
            }
        elif any(word in query_lower for word in ["billing", "charge", "payment", "invoice"]):
            return {
                "intent": "billing",
                "urgency": "medium",
                "entities": ["billing", "payment"],
                "tone": "concerned",
                "keywords": ["billing", "charge", "payment"]
            }
        elif any(word in query_lower for word in ["slow", "loading", "performance", "dashboard"]):
            return {
                "intent": "technical",
                "urgency": "medium",
                "entities": ["dashboard", "performance"],
                "tone": "frustrated",
                "keywords": ["slow", "loading", "performance"]
            }
        elif any(word in query_lower for word in ["slack", "integration", "connect"]):
            return {
                "intent": "feature_request",
                "urgency": "low",
                "entities": ["slack", "integration"],
                "tone": "neutral",
                "keywords": ["slack", "integration", "connect"]
            }
        else:
            return {
                "intent": "general",
                "urgency": "medium",
                "entities": [],
                "tone": "neutral",
                "keywords": user_query.split()[:3]
            }

    def generate_response(self, user_query: str, search_results: List[Dict[str, Any]], user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate smart responses based on query patterns"""
        query_lower = user_query.lower()

        # Password reset
        if any(word in query_lower for word in ["password", "reset", "login"]):
            return {
                "response": "To reset your password: 1) Go to the login page 2) Click 'Forgot Password' 3) Enter your email address 4) Check your email for the reset link 5) Follow the instructions to create a new password. If you don't receive the email within 5 minutes, please check your spam folder.",
                "confidence": 0.95,
                "suggested_actions": ["Try password reset", "Check spam folder", "Contact support if issues persist"],
                "escalate": False,
                "follow_up_questions": ["Are you receiving the reset email?", "Do you need help with two-factor authentication?"]
            }

        # Billing issues
        elif any(word in query_lower for word in ["billing", "charge", "payment"]):
            return {
                "response": "I can help with billing questions. If you were charged twice, this usually happens when: 1) Payment method was updated during billing cycle 2) Failed payment retry succeeded after manual retry. I can help you request a refund for any duplicate charges. Would you like me to walk you through the refund process?",
                "confidence": 0.92,
                "suggested_actions": ["Request refund", "Review billing history", "Update payment method"],
                "escalate": False,
                "follow_up_questions": ["Would you like to see your billing history?", "Do you need help updating your payment method?"]
            }

        # Performance issues
        elif any(word in query_lower for word in ["slow", "loading", "performance"]):
            return {
                "response": "Let's troubleshoot the slow loading issue: 1) Clear your browser cache and cookies 2) Disable browser extensions temporarily 3) Try incognito/private browsing mode 4) Check your internet connection speed. If the issue persists, it might be related to your project size or browser compatibility.",
                "confidence": 0.88,
                "suggested_actions": ["Clear browser cache", "Try incognito mode", "Test internet speed"],
                "escalate": False,
                "follow_up_questions": ["Which browser are you using?", "How large is your current project?"]
            }

        # Slack integration
        elif any(word in query_lower for word in ["slack", "integration"]):
            return {
                "response": "Setting up Slack integration is easy! 1) Go to Settings > Integrations 2) Click 'Add Slack Integration' 3) Authorize CloudFlow in your Slack workspace 4) Choose which channels should receive notifications 5) Configure your notification preferences. You can get updates for project milestones, task assignments, and due dates.",
                "confidence": 0.94,
                "suggested_actions": ["Go to Settings > Integrations", "Authorize Slack workspace", "Configure notifications"],
                "escalate": False,
                "follow_up_questions": ["Which Slack workspace do you want to connect?", "What type of notifications do you want?"]
            }

        # Team permissions
        elif any(word in query_lower for word in ["team", "permission", "access", "edit"]):
            return {
                "response": "For team permissions, CloudFlow has 4 roles: Admin (full access), Manager (edit projects, manage team), Member (view and edit assigned tasks), Viewer (read-only). To change permissions: 1) Go to Team > Members 2) Click on the team member 3) Select their new role. Note: Only Admins can promote other users to Admin level.",
                "confidence": 0.91,
                "suggested_actions": ["Go to Team settings", "Update member roles", "Review permission levels"],
                "escalate": False,
                "follow_up_questions": ["What level of access do they need?", "Should they be able to invite new members?"]
            }

        # Default response
        else:
            return {
                "response": "I'd be happy to help! Could you provide a bit more detail about what you're trying to do? I can assist with account settings, billing questions, integrations, performance issues, and team management.",
                "confidence": 0.75,
                "suggested_actions": ["Provide more details", "Browse help articles", "Contact support"],
                "escalate": False,
                "follow_up_questions": ["What specific feature are you having trouble with?", "Is this related to a recent change in your account?"]
            }

    def enhance_search_query(self, user_query: str, intent_data: Dict[str, Any]) -> str:
        """Enhance search query based on intent"""
        keywords = intent_data.get("keywords", [])
        entities = intent_data.get("entities", [])
        intent = intent_data.get("intent", "general")

        enhanced_terms = [user_query] + keywords + entities + [intent]
        return " ".join(set(enhanced_terms))

    def batch_generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embeddings.append(self.generate_embedding(text))
        return embeddings