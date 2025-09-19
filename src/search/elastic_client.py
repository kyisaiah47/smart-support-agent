from elasticsearch import Elasticsearch
from typing import Dict, List, Any, Optional
import json
from ..config import Config

class ElasticSearchClient:
    def __init__(self):
        self.client = self._create_client()

    def _create_client(self) -> Elasticsearch:
        """Create Elasticsearch client with cloud configuration"""
        if Config.ELASTIC_CLOUD_ID and Config.ELASTIC_PASSWORD:
            return Elasticsearch(
                cloud_id=Config.ELASTIC_CLOUD_ID,
                basic_auth=(Config.ELASTIC_USERNAME, Config.ELASTIC_PASSWORD)
            )
        elif Config.ELASTIC_API_KEY and Config.ELASTIC_ENDPOINT:
            # Elastic Serverless configuration
            return Elasticsearch(
                hosts=[Config.ELASTIC_ENDPOINT],
                api_key=Config.ELASTIC_API_KEY
            )
        elif Config.ELASTIC_API_KEY and Config.ELASTIC_CLOUD_ID:
            # Elastic Cloud with API key
            return Elasticsearch(
                cloud_id=Config.ELASTIC_CLOUD_ID,
                api_key=Config.ELASTIC_API_KEY
            )
        else:
            # Local development fallback
            return Elasticsearch(
                [{"host": "localhost", "port": 9200}]
            )

    def create_knowledge_base_index(self):
        """Create the knowledge base index with proper mappings"""
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "standard"},
                    "content": {"type": "text", "analyzer": "standard"},
                    "category": {"type": "keyword"},
                    "tags": {"type": "keyword"},
                    "last_updated": {"type": "date"},
                    "confidence_score": {"type": "float"},
                    "content_embedding": {
                        "type": "dense_vector",
                        "dims": 768,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }

        try:
            self.client.indices.create(
                index=Config.KNOWLEDGE_BASE_INDEX,
                body=mapping
            )
            print(f"Created index: {Config.KNOWLEDGE_BASE_INDEX}")
        except Exception as e:
            print(f"Index might already exist: {e}")

    def create_support_tickets_index(self):
        """Create the support tickets index"""
        mapping = {
            "mappings": {
                "properties": {
                    "ticket_id": {"type": "keyword"},
                    "problem": {"type": "text", "analyzer": "standard"},
                    "solution": {"type": "text", "analyzer": "standard"},
                    "category": {"type": "keyword"},
                    "priority": {"type": "keyword"},
                    "resolution_time": {"type": "integer"},
                    "satisfaction_score": {"type": "float"},
                    "created_date": {"type": "date"},
                    "problem_embedding": {
                        "type": "dense_vector",
                        "dims": 768,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }

        try:
            self.client.indices.create(
                index=Config.SUPPORT_TICKETS_INDEX,
                body=mapping
            )
            print(f"Created index: {Config.SUPPORT_TICKETS_INDEX}")
        except Exception as e:
            print(f"Index might already exist: {e}")

    def hybrid_search(self,
                     query: str,
                     query_embedding: List[float],
                     index: str,
                     size: int = 5) -> Dict[str, Any]:
        """Perform hybrid search combining keyword and semantic search"""

        search_body = {
            "size": size,
            "query": {
                "bool": {
                    "should": [
                        # Keyword search
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^2", "content", "problem", "solution"],
                                "type": "best_fields",
                                "boost": 1.0
                            }
                        },
                        # Semantic search
                        {
                            "script_score": {
                                "query": {"match_all": {}},
                                "script": {
                                    "source": "cosineSimilarity(params.query_vector, 'content_embedding') + 1.0",
                                    "params": {"query_vector": query_embedding}
                                },
                                "boost": 1.5
                            }
                        }
                    ]
                }
            },
            "_source": ["title", "content", "category", "confidence_score", "problem", "solution"]
        }

        try:
            response = self.client.search(index=index, body=search_body)
            return response
        except Exception as e:
            print(f"Search error: {e}")
            return {"hits": {"hits": []}}

    def index_document(self, index: str, doc_id: str, document: Dict[str, Any]):
        """Index a single document"""
        try:
            self.client.index(index=index, id=doc_id, body=document)
            print(f"Indexed document {doc_id} in {index}")
        except Exception as e:
            print(f"Error indexing document: {e}")

    def bulk_index(self, index: str, documents: List[Dict[str, Any]]):
        """Bulk index multiple documents"""
        actions = []
        for i, doc in enumerate(documents):
            actions.append({
                "_index": index,
                "_id": doc.get("id", i),
                "_source": doc
            })

        try:
            from elasticsearch.helpers import bulk
            bulk(self.client, actions)
            print(f"Bulk indexed {len(documents)} documents to {index}")
        except Exception as e:
            print(f"Bulk index error: {e}")