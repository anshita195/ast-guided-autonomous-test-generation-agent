#!/usr/bin/env python3
"""
AgentForce TestGen Setup Script
Automates the installation and configuration process
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_node_version():
    """Check if Node.js version is compatible"""
    print("🟨 Checking Node.js version...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ Node.js {version} found")
        return True
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    return True

def install_node_dependencies():
    """Install Node.js dependencies"""
    if not run_command("npm install", "Installing Node.js dependencies"):
        return False
    return True

def setup_environment():
    """Set up environment configuration"""
    print("🔧 Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    # Copy example to .env
    shutil.copy(env_example, env_file)
    print("✅ Created .env file from template")
    
    # Prompt for API key
    print("\n🔑 Please enter your Google Gemini API key:")
    print("   Get your API key from: https://aistudio.google.com/app/apikey")
    
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("⚠️  No API key provided. You'll need to edit .env manually")
        return True
    
    # Update .env file with API key
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        
        content = content.replace("your_gemini_api_key_here", api_key)
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ API key configured successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to configure API key: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = ["tests", "js_tests", "coverage"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def verify_installation():
    """Verify the installation"""
    print("🧪 Verifying installation...")
    
    # Test Python imports
    try:
        import fastapi, pytest, coverage, google.generativeai
        print("✅ Python dependencies verified")
    except ImportError as e:
        print(f"❌ Python dependency missing: {e}")
        return False
    
    # Test Node.js dependencies
    try:
        result = subprocess.run(["npm", "list", "jest"], capture_output=True, text=True)
        if "jest" in result.stdout:
            print("✅ Node.js dependencies verified")
        else:
            print("❌ Jest not found in Node.js dependencies")
            return False
    except Exception as e:
        print(f"❌ Failed to verify Node.js dependencies: {e}")
        return False
    
    # Test API import
    try:
        from app.main import app
        print("✅ FastAPI application verified")
    except Exception as e:
        print(f"❌ Failed to import FastAPI application: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 AgentForce TestGen Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_python_dependencies():
        print("❌ Setup failed at Python dependencies")
        sys.exit(1)
    
    if not install_node_dependencies():
        print("❌ Setup failed at Node.js dependencies")
        sys.exit(1)
    
    # Set up environment
    if not setup_environment():
        print("❌ Setup failed at environment configuration")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Verify installation
    if not verify_installation():
        print("❌ Setup verification failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Start the server: python -m uvicorn app.main:app --reload")
    print("2. Visit http://localhost:8000/docs for API documentation")
    print("3. Check README.md for usage examples")
    print("\n🔑 Make sure your GEMINI_API_KEY is configured in .env")

if __name__ == "__main__":
    main()
