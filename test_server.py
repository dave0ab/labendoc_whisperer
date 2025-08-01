#!/usr/bin/env python3
import requests
import sys

def test_server():
    try:
        # Test root endpoint
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Root endpoint status: {response.status_code}")
        
        # Test docs endpoint
        response = requests.get("http://127.0.0.1:8000/docs")
        print(f"Docs endpoint status: {response.status_code}")
        
        # Test openapi.json endpoint
        response = requests.get("http://127.0.0.1:8000/openapi.json")
        print(f"OpenAPI endpoint status: {response.status_code}")
        
        print("✅ Server is running successfully!")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    test_server()