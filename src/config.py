import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Elastic Configuration
    ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
    ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
    ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME", "elastic")
    ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
    ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")

    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Application Configuration
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", 8000))

    # Index Names
    KNOWLEDGE_BASE_INDEX = "cloudflow_knowledge_base"
    SUPPORT_TICKETS_INDEX = "cloudflow_support_tickets"
    PRODUCT_CATALOG_INDEX = "cloudflow_product_catalog"