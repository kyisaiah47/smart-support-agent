"""
Core support agent logic integrating search and AI
"""
from typing import Dict, List, Any, Optional
from ..search import ElasticSearchClient
from ..ai import GeminiClient
from ..config import Config
import uuid
from datetime import datetime

class SupportAgent:
    def __init__(self):
        self.elastic_client = ElasticSearchClient()
        self.ai_client = GeminiClient()
        self.conversation_history: Dict[str, List[Dict]] = {}

    def process_query(self,
                     user_query: str,
                     session_id: str = None,
                     user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main method to process user query and generate response
        """
        if not session_id:
            session_id = str(uuid.uuid4())

        # Initialize conversation history for new sessions
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []

        try:
            # Step 1: Analyze user intent
            intent_data = self.ai_client.analyze_intent(user_query)

            # Step 2: Enhance search query
            enhanced_query = self.ai_client.enhance_search_query(user_query, intent_data)

            # Step 3: Generate query embedding
            query_embedding = self.ai_client.generate_embedding(user_query)

            # Step 4: Search knowledge base
            kb_results = self.elastic_client.hybrid_search(
                query=enhanced_query,
                query_embedding=query_embedding,
                index=Config.KNOWLEDGE_BASE_INDEX,
                size=5
            )

            # Step 5: Search support tickets for similar issues
            ticket_results = self.elastic_client.hybrid_search(
                query=enhanced_query,
                query_embedding=query_embedding,
                index=Config.SUPPORT_TICKETS_INDEX,
                size=3
            )

            # Step 6: Combine search results
            all_results = self._combine_search_results(kb_results, ticket_results)

            # Step 7: Generate response using AI
            response_data = self.ai_client.generate_response(
                user_query=user_query,
                search_results=all_results,
                user_context=user_context
            )

            # Step 8: Store conversation
            conversation_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_query": user_query,
                "intent": intent_data,
                "response": response_data,
                "search_results_count": len(all_results)
            }
            self.conversation_history[session_id].append(conversation_entry)

            # Step 9: Format final response
            final_response = {
                "session_id": session_id,
                "response": response_data.get("response", "I'm sorry, I couldn't generate a proper response."),
                "confidence": response_data.get("confidence", 0.5),
                "intent": intent_data,
                "suggested_actions": response_data.get("suggested_actions", []),
                "escalate": response_data.get("escalate", False),
                "follow_up_questions": response_data.get("follow_up_questions", []),
                "sources": self._format_sources(all_results[:2]),  # Top 2 sources
                "timestamp": datetime.now().isoformat()
            }

            return final_response

        except Exception as e:
            print(f"Error processing query: {e}")
            return self._error_response(session_id, user_query)

    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        return self.conversation_history.get(session_id, [])

    def _combine_search_results(self,
                               kb_results: Dict[str, Any],
                               ticket_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Combine and deduplicate search results from different indices"""
        combined = []

        # Add knowledge base results with source tagging
        for hit in kb_results.get("hits", {}).get("hits", []):
            hit["_source"]["result_type"] = "knowledge_base"
            combined.append(hit)

        # Add ticket results with source tagging
        for hit in ticket_results.get("hits", {}).get("hits", []):
            hit["_source"]["result_type"] = "support_ticket"
            combined.append(hit)

        # Sort by relevance score
        combined.sort(key=lambda x: x.get("_score", 0), reverse=True)

        return combined

    def _format_sources(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format search results as source references"""
        sources = []
        for result in search_results:
            source = result.get("_source", {})
            result_type = source.get("result_type", "unknown")

            if result_type == "knowledge_base":
                sources.append({
                    "title": source.get("title", "Knowledge Base Article"),
                    "type": "Knowledge Base",
                    "category": source.get("category", "general"),
                    "relevance": f"{result.get('_score', 0):.2f}"
                })
            elif result_type == "support_ticket":
                sources.append({
                    "title": f"Similar Issue: {source.get('problem', 'Unknown')[:50]}...",
                    "type": "Support Ticket",
                    "category": source.get("category", "general"),
                    "relevance": f"{result.get('_score', 0):.2f}"
                })

        return sources

    def _error_response(self, session_id: str, user_query: str) -> Dict[str, Any]:
        """Generate error response when processing fails"""
        return {
            "session_id": session_id,
            "response": "I apologize, but I'm experiencing technical difficulties. Please try rephrasing your question or contact our human support team for immediate assistance.",
            "confidence": 0.0,
            "intent": {"intent": "unknown", "urgency": "medium"},
            "suggested_actions": ["Contact human support", "Try rephrasing your question"],
            "escalate": True,
            "follow_up_questions": [],
            "sources": [],
            "timestamp": datetime.now().isoformat(),
            "error": True
        }

    def get_suggested_questions(self) -> List[str]:
        """Get list of suggested questions for users"""
        return [
            "How do I reset my password?",
            "Why was I charged twice this month?",
            "How can I integrate CloudFlow with Slack?",
            "My dashboard is loading slowly, what should I do?",
            "How do I manage team permissions?",
            "How can I cancel my subscription?",
            "How do I export my project data?",
            "How do I set up two-factor authentication?"
        ]

    def analyze_conversation_trends(self) -> Dict[str, Any]:
        """Analyze conversation trends across all sessions"""
        total_conversations = sum(len(history) for history in self.conversation_history.values())
        if total_conversations == 0:
            return {"total_conversations": 0}

        intents = []
        confidence_scores = []
        escalations = 0

        for session_history in self.conversation_history.values():
            for entry in session_history:
                intent_data = entry.get("intent", {})
                response_data = entry.get("response", {})

                intents.append(intent_data.get("intent", "unknown"))
                confidence_scores.append(response_data.get("confidence", 0))
                if response_data.get("escalate", False):
                    escalations += 1

        # Calculate metrics
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        escalation_rate = (escalations / total_conversations) * 100 if total_conversations > 0 else 0

        # Count intent categories
        intent_counts = {}
        for intent in intents:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1

        return {
            "total_conversations": total_conversations,
            "average_confidence": round(avg_confidence, 2),
            "escalation_rate": round(escalation_rate, 2),
            "top_intents": sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "active_sessions": len(self.conversation_history)
        }