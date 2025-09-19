"""
Simple Gemini client using direct API calls
"""
import requests
import json
from typing import List, Dict, Any
from ..config import Config
import subprocess

class GeminiClient:
    def __init__(self):
        self.project_id = Config.GOOGLE_CLOUD_PROJECT
        self.location = "us-central1"
        self.model_id = "gemini-1.5-pro-002"

    def _get_access_token(self):
        """Get access token using gcloud"""
        try:
            result = subprocess.run(
                ["gcloud", "auth", "application-default", "print-access-token"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        # Return a dummy embedding for now - embeddings work via different endpoint
        import random
        random.seed(hash(text))
        return [random.uniform(-1, 1) for _ in range(768)]

    def analyze_intent(self, user_query: str) -> Dict[str, Any]:
        """Analyze user intent using Gemini API"""
        access_token = self._get_access_token()
        if not access_token:
            return self._fallback_intent()

        url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_id}:generateContent"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Analyze this customer support query and extract:
        1. Intent category (billing, technical, account, feature_request, general)
        2. Urgency level (low, medium, high, critical)
        3. Key entities mentioned
        4. Emotional tone (frustrated, neutral, positive)

        Query: "{user_query}"

        Return only valid JSON:
        {{
            "intent": "category",
            "urgency": "level",
            "entities": ["entity1", "entity2"],
            "tone": "emotional_state",
            "keywords": ["key1", "key2"]
        }}
        """

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "topP": 0.95,
                "topK": 20,
                "maxOutputTokens": 1024
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                text_response = result["candidates"][0]["content"]["parts"][0]["text"]

                # Try to extract JSON
                try:
                    if "```json" in text_response:
                        json_str = text_response.split("```json")[1].split("```")[0]
                    elif "{" in text_response:
                        json_str = text_response[text_response.find("{"):text_response.rfind("}")+1]
                    else:
                        json_str = text_response

                    return json.loads(json_str.strip())
                except:
                    return self._fallback_intent()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._fallback_intent()
        except Exception as e:
            print(f"Request error: {e}")
            return self._fallback_intent()

    def generate_response(self, user_query: str, search_results: List[Dict[str, Any]], user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate response using Gemini API"""
        access_token = self._get_access_token()
        if not access_token:
            return self._fallback_response()

        # Format search results
        context_docs = []
        for result in search_results[:3]:
            source = result.get("_source", {})
            doc_text = f"Title: {source.get('title', 'N/A')}\n"
            doc_text += f"Content: {source.get('content', source.get('solution', 'N/A'))}"
            context_docs.append(doc_text)

        context = "\n\n---\n\n".join(context_docs) if context_docs else "No specific documentation found."

        prompt = f"""
        You are a helpful customer support agent for CloudFlow, a project management SaaS platform.

        Customer Question: "{user_query}"

        Relevant Knowledge Base:
        {context}

        Instructions:
        1. Provide a helpful, accurate response
        2. Be conversational and empathetic
        3. If information isn't sufficient, ask clarifying questions
        4. Keep responses concise but complete

        Response format (JSON only):
        {{
            "response": "Your helpful response here",
            "confidence": 0.95,
            "suggested_actions": ["action1", "action2"],
            "escalate": false,
            "follow_up_questions": ["question1"]
        }}
        """

        url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_id}:generateContent"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "topP": 0.95,
                "topK": 20,
                "maxOutputTokens": 1024
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                text_response = result["candidates"][0]["content"]["parts"][0]["text"]

                # Try to extract JSON
                try:
                    if "```json" in text_response:
                        json_str = text_response.split("```json")[1].split("```")[0]
                    elif "{" in text_response:
                        json_str = text_response[text_response.find("{"):text_response.rfind("}")+1]
                    else:
                        json_str = text_response

                    parsed = json.loads(json_str.strip())
                    return parsed
                except:
                    # If JSON parsing fails, return the text as response
                    return {
                        "response": text_response.strip(),
                        "confidence": 0.8,
                        "suggested_actions": [],
                        "escalate": False,
                        "follow_up_questions": []
                    }
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._fallback_response()
        except Exception as e:
            print(f"Request error: {e}")
            return self._fallback_response()

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

    def _fallback_intent(self):
        return {
            "intent": "general",
            "urgency": "medium",
            "entities": [],
            "tone": "neutral",
            "keywords": []
        }

    def _fallback_response(self):
        return {
            "response": "I understand you need help. Let me connect you with a human agent who can assist you better.",
            "confidence": 0.1,
            "suggested_actions": ["Contact human support"],
            "escalate": True,
            "follow_up_questions": []
        }