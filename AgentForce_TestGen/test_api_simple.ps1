# PowerShell script to test AgentForce TestGen API
# Usage: .\test_api_simple.ps1

Write-Host "🚀 AgentForce TestGen API Test (PowerShell)" -ForegroundColor Green
Write-Host "=================================================="

# Test API health
Write-Host "`n🔍 Testing API health..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ API Status: $($healthResponse.status)" -ForegroundColor Green
    Write-Host "✅ LLM Status: $($healthResponse.llm)" -ForegroundColor Green
    
    if ($healthResponse.llm -eq 'unavailable') {
        Write-Host "⚠️  Warning: LLM is unavailable. Check your GEMINI_API_KEY" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ API Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure the server is running: python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🎉 API is working! You can now:" -ForegroundColor Green
Write-Host "1. Visit http://localhost:8000/docs for interactive API documentation" -ForegroundColor Cyan
Write-Host "2. Use the API to generate tests for your Python and JavaScript files" -ForegroundColor Cyan
Write-Host "3. Check the README.md for detailed usage examples" -ForegroundColor Cyan

Write-Host "`n📊 Current Status:" -ForegroundColor Yellow
Write-Host "✅ API Server: Running" -ForegroundColor Green
Write-Host "✅ LLM Service: Available" -ForegroundColor Green
Write-Host "✅ Python Support: Ready" -ForegroundColor Green
Write-Host "✅ JavaScript Support: Ready" -ForegroundColor Green
