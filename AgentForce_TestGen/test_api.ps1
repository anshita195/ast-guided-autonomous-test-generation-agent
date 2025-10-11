# PowerShell script to test AgentForce TestGen API
# Usage: .\test_api.ps1

Write-Host "🚀 AgentForce TestGen API Test (PowerShell)" -ForegroundColor Green
Write-Host "=" * 50

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

# Test Python generation
Write-Host "`n🐍 Testing Python test generation..." -ForegroundColor Yellow
try {
    $pythonFile = "examples\sample_input.py"
    if (-not (Test-Path $pythonFile)) {
        Write-Host "❌ Python example file not found: $pythonFile" -ForegroundColor Red
        exit 1
    }
    
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = (
        "--$boundary",
        "Content-Disposition: form-data; name=`"language`"",
        "",
        "python",
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"sample_input.py`"",
        "Content-Type: application/octet-stream",
        "",
        [System.IO.File]::ReadAllText($pythonFile),
        "--$boundary--",
        ""
    ) -join $LF
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/generate" -Method Post -Body $bodyLines -ContentType "multipart/form-data; boundary=$boundary"
    
    Write-Host "✅ Language: $($response.language)" -ForegroundColor Green
    Write-Host "✅ Functions Found: $($response.functions_found)" -ForegroundColor Green
    Write-Host "✅ Test File: $($response.test_file_path)" -ForegroundColor Green
    
    $coverage = $response.coverage_report
    $coveragePct = if ($coverage.coverage_percentage) { "$($coverage.coverage_percentage)%" } else { "N/A" }
    Write-Host "✅ Coverage: $coveragePct" -ForegroundColor Green
    Write-Host "✅ Status: $($coverage.status)" -ForegroundColor Green
    Write-Host "✅ Summary: $($coverage.summary)" -ForegroundColor Green
    
    $pythonSuccess = $true
} catch {
    Write-Host "❌ Python Generation Failed: $($_.Exception.Message)" -ForegroundColor Red
    $pythonSuccess = $false
}

# Test JavaScript generation
Write-Host "`n🟨 Testing JavaScript test generation..." -ForegroundColor Yellow
try {
    $jsFile = "examples\sample_input.js"
    if (-not (Test-Path $jsFile)) {
        Write-Host "❌ JavaScript example file not found: $jsFile" -ForegroundColor Red
        exit 1
    }
    
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = (
        "--$boundary",
        "Content-Disposition: form-data; name=`"language`"",
        "",
        "javascript",
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"sample_input.js`"",
        "Content-Type: application/octet-stream",
        "",
        [System.IO.File]::ReadAllText($jsFile),
        "--$boundary--",
        ""
    ) -join $LF
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/generate" -Method Post -Body $bodyLines -ContentType "multipart/form-data; boundary=$boundary"
    
    Write-Host "✅ Language: $($response.language)" -ForegroundColor Green
    Write-Host "✅ Functions Found: $($response.functions_found)" -ForegroundColor Green
    Write-Host "✅ Test File: $($response.test_file_path)" -ForegroundColor Green
    
    $coverage = $response.coverage_report
    $coveragePct = if ($coverage.coverage_percentage) { "$($coverage.coverage_percentage)%" } else { "N/A" }
    Write-Host "✅ Coverage: $coveragePct" -ForegroundColor Green
    Write-Host "✅ Status: $($coverage.status)" -ForegroundColor Green
    Write-Host "✅ Summary: $($coverage.summary)" -ForegroundColor Green
    
    $jsSuccess = $true
} catch {
    Write-Host "❌ JavaScript Generation Failed: $($_.Exception.Message)" -ForegroundColor Red
    $jsSuccess = $false
}

# Summary
Write-Host "`n" + "=" * 50 -ForegroundColor Green
$totalTests = 2
$passedTests = if ($pythonSuccess) { 1 } else { 0 } + if ($jsSuccess) { 1 } else { 0 }

Write-Host "📊 Test Results: $passedTests/$totalTests tests passed" -ForegroundColor Cyan

if ($passedTests -eq $totalTests) {
    Write-Host "🎉 All tests passed! API is working correctly." -ForegroundColor Green
} else {
    Write-Host "⚠️  Some tests failed. Check the output above for details." -ForegroundColor Yellow
}

Write-Host "`n📖 You can also visit http://localhost:8000/docs for interactive API documentation" -ForegroundColor Cyan
