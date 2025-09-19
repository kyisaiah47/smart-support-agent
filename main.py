#!/usr/bin/env python3
"""
Main entry point for the Smart Customer Support Agent
"""
import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_data():
    """Load sample data into Elasticsearch"""
    from src.data import DataLoader

    print("Setting up sample data...")
    loader = DataLoader()
    loader.load_all_data()
    print("Data setup complete!")

def run_server():
    """Run the FastAPI server"""
    import uvicorn
    from src.config import Config

    print("Starting Smart Customer Support Agent...")
    print(f"Server will be available at: http://{Config.API_HOST}:{Config.API_PORT}")
    print("API docs available at: http://{Config.API_HOST}:{Config.API_PORT}/docs")

    uvicorn.run(
        "src.api.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=True
    )

def run_tests():
    """Run test queries"""
    from src.data import DataLoader

    print("Running test queries...")
    loader = DataLoader()

    test_queries = [
        "How do I reset my password?",
        "Why was I charged twice this month?",
        "My Slack integration isn't working",
        "Dashboard is loading slowly",
        "How do I manage team permissions?"
    ]

    for query in test_queries:
        print(f"\n{'='*50}")
        loader.search_test(query)

def main():
    parser = argparse.ArgumentParser(description="Smart Customer Support Agent")
    parser.add_argument(
        'command',
        choices=['setup', 'run', 'test'],
        help='Command to execute'
    )

    args = parser.parse_args()

    if args.command == 'setup':
        setup_data()
    elif args.command == 'run':
        run_server()
    elif args.command == 'test':
        run_tests()

if __name__ == "__main__":
    main()