import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel
from typing import List, Dict, Any
import json
from ..config import Config

class GeminiClient:
    def __init__(self):
        vertexai.init(project=Config.GOOGLE_CLOUD_PROJECT, location="us-central1")
        self.model = GenerativeModel("gemini-1.5-pro-002")
        self.embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using Vertex AI"""
        try:
            embeddings = self.embedding_model.get_embeddings([text])
            return embeddings[0].values
        except Exception as e:
            print(f"Embedding generation error: {e}")
            return [0.0] * 768  # Return zero vector as fallback

    def analyze_intent(self, user_query: str) -> Dict[str, Any]:
        """Analyze user intent and extract key information"""
        prompt = f"""
        Analyze this customer support query and extract:
        1. Intent category (billing, technical, account, feature_request, general)
        2. Urgency level (low, medium, high, critical)
        3. Key entities mentioned (product names, error codes, etc.)
        4. Emotional tone (frustrated, neutral, positive)

        Query: "{user_query}"

        Return as JSON:
        {{
            "intent": "category",
            "urgency": "level",
            "entities": ["entity1", "entity2"],
            "tone": "emotional_state",
            "keywords": ["key1", "key2"]
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # Try to extract JSON from response
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]

            return json.loads(response_text)
        except Exception as e:
            print(f"Intent analysis error: {e}")
            return {
                "intent": "general",
                "urgency": "medium",
                "entities": [],
                "tone": "neutral",
                "keywords": user_query.split()[:5]
            }

    def enhance_search_query(self, user_query: str, intent_data: Dict[str, Any]) -> str:
        """Enhance search query based on intent analysis"""
        keywords = intent_data.get("keywords", [])
        entities = intent_data.get("entities", [])
        intent = intent_data.get("intent", "general")

        # Combine original query with extracted keywords and entities
        enhanced_terms = [user_query] + keywords + entities + [intent]
        return " ".join(set(enhanced_terms))

    def generate_response(self,
                         user_query: str,
                         search_results: List[Dict[str, Any]],
                         user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate contextual response using search results"""

        # Format search results for context
        context_docs = []
        for result in search_results[:3]:  # Use top 3 results
            source = result.get("_source", {})
            doc_text = f"Title: {source.get('title', 'N/A')}\n"
            doc_text += f"Content: {source.get('content', source.get('solution', 'N/A'))}\n"
            doc_text += f"Category: {source.get('category', 'N/A')}"
            context_docs.append(doc_text)

        context = "\n\n---\n\n".join(context_docs)

        user_info = ""
        if user_context:
            user_info = f"User context: {user_context.get('subscription_tier', 'Free')} plan, "
            user_info += f"Previous issues: {user_context.get('issue_history', 'None')}"

        prompt = f"""
        You are a helpful customer support agent for CloudFlow, a project management SaaS platform.

        Customer Question: "{user_query}"

        {user_info}

        Relevant Knowledge Base Information:
        {context}

        Instructions:
        1. Provide a helpful, accurate response based on the knowledge base
        2. Be conversational and empathetic
        3. If the information isn't sufficient, ask clarifying questions
        4. Suggest next steps or escalation if needed
        5. Keep responses concise but complete

        Response format:
        {{
            "response": "Your helpful response here",
            "confidence": 0.95,
            "suggested_actions": ["action1", "action2"],
            "escalate": false,
            "follow_up_questions": ["question1", "question2"]
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]

            return json.loads(response_text)
        except Exception as e:
            print(f"Response generation error: {e}")
            return {
                "response": "I understand you need help. Let me connect you with a human agent who can assist you better.",
                "confidence": 0.1,
                "suggested_actions": ["Contact human support"],
                "escalate": True,
                "follow_up_questions": []
            }

    def batch_generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches"""
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                batch_embeddings = self.embedding_model.get_embeddings(batch)
                embeddings.extend([emb.values for emb in batch_embeddings])
            except Exception as e:
                print(f"Batch embedding error: {e}")
                # Add zero vectors for failed batch
                embeddings.extend([[0.0] * 768] * len(batch))

        return embeddings