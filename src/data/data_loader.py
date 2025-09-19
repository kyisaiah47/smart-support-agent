"""
Data loading and indexing utilities
"""
from typing import List, Dict, Any
from ..search import ElasticSearchClient
from ..ai import GeminiClient
from .sample_data import KNOWLEDGE_BASE_DATA, SUPPORT_TICKETS_DATA, PRODUCT_CATALOG_DATA
from ..config import Config
import time

class DataLoader:
    def __init__(self):
        self.elastic_client = ElasticSearchClient()
        self.ai_client = GeminiClient()

    def setup_indices(self):
        """Create all necessary indices"""
        print("Creating Elasticsearch indices...")
        self.elastic_client.create_knowledge_base_index()
        self.elastic_client.create_support_tickets_index()
        print("Indices created successfully!")

    def load_knowledge_base(self):
        """Load knowledge base data with embeddings"""
        print("Loading knowledge base data...")

        # Generate embeddings for all knowledge base content
        texts = [f"{item['title']} {item['content']}" for item in KNOWLEDGE_BASE_DATA]
        print("Generating embeddings...")
        embeddings = self.ai_client.batch_generate_embeddings(texts)

        # Add embeddings to documents
        documents_with_embeddings = []
        for i, item in enumerate(KNOWLEDGE_BASE_DATA):
            doc = item.copy()
            doc['content_embedding'] = embeddings[i]
            documents_with_embeddings.append(doc)

        # Index documents
        self.elastic_client.bulk_index(
            Config.KNOWLEDGE_BASE_INDEX,
            documents_with_embeddings
        )
        print(f"Loaded {len(documents_with_embeddings)} knowledge base articles")

    def load_support_tickets(self):
        """Load historical support tickets with embeddings"""
        print("Loading support tickets...")

        # Generate embeddings for problem descriptions
        texts = [item['problem'] for item in SUPPORT_TICKETS_DATA]
        print("Generating problem embeddings...")
        embeddings = self.ai_client.batch_generate_embeddings(texts)

        # Add embeddings to documents
        documents_with_embeddings = []
        for i, item in enumerate(SUPPORT_TICKETS_DATA):
            doc = item.copy()
            doc['problem_embedding'] = embeddings[i]
            documents_with_embeddings.append(doc)

        # Index documents
        self.elastic_client.bulk_index(
            Config.SUPPORT_TICKETS_INDEX,
            documents_with_embeddings
        )
        print(f"Loaded {len(documents_with_embeddings)} support tickets")

    def load_product_catalog(self):
        """Load product catalog data"""
        print("Loading product catalog...")

        # For product catalog, we'll use the knowledge base index with category "product"
        product_docs = []
        for item in PRODUCT_CATALOG_DATA:
            doc = {
                "id": item["id"],
                "title": f"{item['product_name']} - {item['price']}",
                "content": f"{item['description']} Features: {', '.join(item['features'])}. {item['troubleshooting']}",
                "category": "product",
                "tags": ["product", "pricing", "features"],
                "confidence_score": 0.95
            }
            product_docs.append(doc)

        # Generate embeddings
        texts = [f"{doc['title']} {doc['content']}" for doc in product_docs]
        embeddings = self.ai_client.batch_generate_embeddings(texts)

        # Add embeddings
        for i, doc in enumerate(product_docs):
            doc['content_embedding'] = embeddings[i]

        # Index documents
        self.elastic_client.bulk_index(Config.KNOWLEDGE_BASE_INDEX, product_docs)
        print(f"Loaded {len(product_docs)} product catalog items")

    def load_all_data(self):
        """Load all sample data"""
        print("Starting data loading process...")

        # Setup indices first
        self.setup_indices()

        # Small delay to ensure indices are ready
        time.sleep(2)

        # Load all data
        self.load_knowledge_base()
        self.load_support_tickets()
        self.load_product_catalog()

        print("All data loaded successfully!")
        print("\nData Summary:")
        print(f"- Knowledge Base: {len(KNOWLEDGE_BASE_DATA)} articles")
        print(f"- Support Tickets: {len(SUPPORT_TICKETS_DATA)} tickets")
        print(f"- Product Catalog: {len(PRODUCT_CATALOG_DATA)} products")

    def search_test(self, query: str):
        """Test search functionality"""
        print(f"\nTesting search for: '{query}'")

        # Generate query embedding
        query_embedding = self.ai_client.generate_embedding(query)

        # Search knowledge base
        results = self.elastic_client.hybrid_search(
            query=query,
            query_embedding=query_embedding,
            index=Config.KNOWLEDGE_BASE_INDEX,
            size=3
        )

        print(f"Found {len(results['hits']['hits'])} results:")
        for hit in results['hits']['hits']:
            source = hit['_source']
            print(f"- {source.get('title', 'No title')} (Score: {hit['_score']:.2f})")
            print(f"  Category: {source.get('category', 'N/A')}")
            print(f"  Content preview: {source.get('content', '')[:100]}...")
            print()

if __name__ == "__main__":
    loader = DataLoader()

    # Load all data
    loader.load_all_data()

    # Test searches
    test_queries = [
        "How do I reset my password?",
        "billing problem",
        "Slack integration",
        "dashboard slow"
    ]

    for query in test_queries:
        loader.search_test(query)