from setuptools import setup, find_packages

setup(
    name="smart-support-agent",
    version="1.0.0",
    description="AI-powered customer support agent using Elastic Search + Google Cloud AI",
    author="Hackathon Team",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "elasticsearch==8.11.0",
        "google-cloud-aiplatform==1.38.1",
        "google-cloud-storage==2.10.0",
        "pydantic==2.5.0",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "numpy==1.25.2"
    ],
    entry_points={
        "console_scripts": [
            "support-agent=main:main",
        ],
    },
)