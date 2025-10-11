#!/bin/bash

echo "🚀 AgentForce TestGen Setup (Linux/macOS)"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install Python dependencies
echo "🔧 Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
echo "🔧 Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating environment configuration..."
    cp env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "🔑 Please edit .env file and add your GEMINI_API_KEY"
    echo "   Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
    read -p "Press Enter to continue..."
fi

# Create necessary directories
mkdir -p tests js_tests coverage

echo "🎉 Setup completed successfully!"
echo ""
echo "📖 Next steps:"
echo "1. Edit .env file and add your GEMINI_API_KEY"
echo "2. Start the server: python3 -m uvicorn app.main:app --reload"
echo "3. Visit http://localhost:8000/docs for API documentation"
echo ""
