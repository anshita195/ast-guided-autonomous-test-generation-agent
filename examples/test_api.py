#!/usr/bin/env python3
"""
Test script for AgentForce TestGen API
Demonstrates how to use the API programmatically
"""

import requests
import json
import os
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
EXAMPLES_DIR = Path("examples")

def test_api_health():
    """Test the health endpoint"""
    print("🔍 Testing API health...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ API Status: {data['status']}")
        print(f"✅ LLM Status: {data['llm']}")
        
        if data['llm'] == 'unavailable':
            print("⚠️  Warning: LLM is unavailable. Check your GEMINI_API_KEY")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Health Check Failed: {e}")
        return False

def test_python_generation():
    """Test Python test generation"""
    print("\n🐍 Testing Python test generation...")
    
    python_file = EXAMPLES_DIR / "sample_input.py"
    if not python_file.exists():
        print(f"❌ Python example file not found: {python_file}")
        return False
    
    try:
        with open(python_file, 'rb') as f:
            files = {'file': f}
            data = {'language': 'python'}
            
            response = requests.post(
                f"{API_BASE_URL}/generate",
                files=files,
                data=data
            )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Language: {result['language']}")
        print(f"✅ Functions Found: {result['functions_found']}")
        print(f"✅ Test File: {result['test_file_path']}")
        
        coverage = result['coverage_report']
        coverage_pct = coverage.get('coverage_percentage', 'N/A')
        print(f"✅ Coverage: {coverage_pct}%")
        print(f"✅ Status: {coverage['status']}")
        print(f"✅ Summary: {coverage['summary']}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Python Generation Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"   Error Details: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Error Response: {e.response.text}")
        return False

def test_javascript_generation():
    """Test JavaScript test generation"""
    print("\n🟨 Testing JavaScript test generation...")
    
    js_file = EXAMPLES_DIR / "sample_input.js"
    if not js_file.exists():
        print(f"❌ JavaScript example file not found: {js_file}")
        return False
    
    try:
        with open(js_file, 'rb') as f:
            files = {'file': f}
            data = {'language': 'javascript'}
            
            response = requests.post(
                f"{API_BASE_URL}/generate",
                files=files,
                data=data
            )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Language: {result['language']}")
        print(f"✅ Functions Found: {result['functions_found']}")
        print(f"✅ Test File: {result['test_file_path']}")
        
        coverage = result['coverage_report']
        coverage_pct = coverage.get('coverage_percentage', 'N/A')
        print(f"✅ Coverage: {coverage_pct}%")
        print(f"✅ Status: {coverage['status']}")
        print(f"✅ Summary: {coverage['summary']}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ JavaScript Generation Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"   Error Details: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Error Response: {e.response.text}")
        return False

def test_error_handling():
    """Test error handling scenarios"""
    print("\n🚨 Testing error handling...")
    
    # Test 1: Invalid language
    print("  Testing invalid language...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate",
            files={'file': open(EXAMPLES_DIR / "sample_input.py", 'rb')},
            data={'language': 'invalid'}
        )
        
        if response.status_code == 400:
            print("  ✅ Invalid language properly rejected")
        else:
            print(f"  ❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error testing invalid language: {e}")
    
    # Test 2: No file provided
    print("  Testing missing file...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate",
            data={'language': 'python'}
        )
        
        if response.status_code == 422:  # FastAPI validation error
            print("  ✅ Missing file properly rejected")
        else:
            print(f"  ❌ Expected 422, got {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error testing missing file: {e}")

def main():
    """Run all API tests"""
    print("🚀 AgentForce TestGen API Test Suite")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ API is running at {API_BASE_URL}")
    except requests.exceptions.RequestException:
        print(f"❌ API is not running at {API_BASE_URL}")
        print("   Please start the server with: python -m uvicorn app.main:app --reload")
        return
    
    # Run tests
    tests_passed = 0
    total_tests = 0
    
    # Health check
    total_tests += 1
    if test_api_health():
        tests_passed += 1
    
    # Python generation
    total_tests += 1
    if test_python_generation():
        tests_passed += 1
    
    # JavaScript generation
    total_tests += 1
    if test_javascript_generation():
        tests_passed += 1
    
    # Error handling
    test_error_handling()
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
