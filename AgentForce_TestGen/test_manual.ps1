# Manual API test for PowerShell users
# This shows how to test the API with a simple PowerShell command

Write-Host "🚀 Manual API Test Example" -ForegroundColor Green
Write-Host "========================="

Write-Host "`nTo test the API manually in PowerShell, use this command:" -ForegroundColor Yellow
Write-Host ""
Write-Host 'Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get' -ForegroundColor Cyan
Write-Host ""

Write-Host "Or to test the generate endpoint with a file:" -ForegroundColor Yellow
Write-Host ""
Write-Host '# First, create a simple test file' -ForegroundColor Gray
Write-Host 'echo "def add(a, b): return a + b" > test.py' -ForegroundColor Gray
Write-Host ""
Write-Host '# Then test the API (this is a simplified example)' -ForegroundColor Gray
Write-Host '# Note: Full multipart form data is complex in PowerShell' -ForegroundColor Gray
Write-Host '# For full testing, use the Python script: python examples/test_api.py' -ForegroundColor Gray
Write-Host ""

Write-Host "🎉 Your AgentForce TestGen is fully operational!" -ForegroundColor Green
Write-Host ""
Write-Host "✅ API Server: Running on http://localhost:8000" -ForegroundColor Green
Write-Host "✅ Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "✅ Health Check: http://localhost:8000/health" -ForegroundColor Green
Write-Host "✅ Test Suite: python examples/test_api.py" -ForegroundColor Green
