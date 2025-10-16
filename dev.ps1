# PowerShell Development Script for Windows
# This is a Windows equivalent of the macOS dev.sh script

param(
    [Parameter(Position=0)]
    [string]$Command = "start",
    [switch]$NoBrowser
)

# Configuration
$FrontendPort = 3000
$BackendPort = 8000
$FrontendDir = "frontend"
$BackendDir = "backend"
$LogDir = "logs"
$PidFile = "dev.pid"
$OpenBrowser = !$NoBrowser  # Disable if --NoBrowser flag is used

# Create logs directory if it doesn't exist
if (!(Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

# Function to print colored output
function Write-Status {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
}

function Write-Header {
    Write-Host "=============================================================================" -ForegroundColor White
    Write-Host "🚀 Gemini LaTeX Enhancer - Development Environment" -ForegroundColor White
    Write-Host "=============================================================================" -ForegroundColor White
    Write-Host "Frontend: http://localhost:$FrontendPort" -ForegroundColor Cyan
    Write-Host "Backend:  http://localhost:$BackendPort" -ForegroundColor Cyan
    Write-Host "Health:   http://localhost:$BackendPort/health" -ForegroundColor Cyan
    Write-Host "=============================================================================" -ForegroundColor White
}

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Function to kill processes on specific ports
function Stop-Port {
    param([int]$Port)
    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        if ($processes) {
            Write-Status "Killing processes on port $Port..." "Yellow"
            $processes | ForEach-Object { 
                Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue 
            }
            Start-Sleep -Seconds 1
        }
    }
    catch {
        # Ignore errors
    }
}

# Function to check if Python virtual environment exists
function Test-PythonEnv {
    if (!(Test-Path "$BackendDir\venv")) {
        Write-Status "❌ Python virtual environment not found!" "Red"
        Write-Status "Creating virtual environment..." "Yellow"
        Set-Location $BackendDir
        python -m venv venv
        Set-Location ..
        Write-Status "✅ Virtual environment created" "Green"
    }
}

# Function to check if Node modules exist
function Test-NodeModules {
    if (!(Test-Path "$FrontendDir\node_modules")) {
        Write-Status "❌ Node modules not found!" "Red"
        Write-Status "Installing dependencies..." "Yellow"
        Set-Location $FrontendDir
        npm install
        Set-Location ..
        Write-Status "✅ Dependencies installed" "Green"
    }
}

# Function to install Python dependencies
function Install-PythonDeps {
    Write-Status "Installing Python dependencies..." "Yellow"
    Set-Location $BackendDir
    & ".\venv\Scripts\Activate.ps1"
    pip install -r requirements.txt
    Set-Location ..
    Write-Status "✅ Python dependencies installed" "Green"
}

# Function to start backend
function Start-Backend {
    Write-Status "🐍 Starting FastAPI backend..." "Blue"
    
    Set-Location $BackendDir
    & ".\venv\Scripts\Activate.ps1"
    
    # Check if GEMINI_API_KEY is set
    if (!$env:GEMINI_API_KEY) {
        if (Test-Path "..\.env") {
            Write-Status "⚠️  GEMINI_API_KEY not found in environment variables" "Yellow"
            Write-Status "💡 Found .env file in root directory - the backend will load it automatically" "Cyan"
        } else {
            Write-Status "⚠️  GEMINI_API_KEY not set. Please set it in your environment or create .env file in root directory" "Yellow"
        }
    } else {
        Write-Status "✅ GEMINI_API_KEY found in environment" "Green"
    }
    
    # Start the backend
    $backendJob = Start-Job -ScriptBlock {
        param($BackendDir, $BackendPort, $LogDir)
        Set-Location $BackendDir
        & ".\venv\Scripts\Activate.ps1"
        python -m uvicorn app.main:app --host 0.0.0.0 --port $BackendPort --reload
    } -ArgumentList (Resolve-Path $BackendDir), $BackendPort, $LogDir
    
    $backendJob.Id | Out-File -FilePath "..\$PidFile.backend" -Encoding ASCII
    
    Set-Location ..
    
    # Wait for backend to start
    Write-Status "Waiting for backend to start..." "Yellow"
    for ($i = 1; $i -le 30; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$BackendPort/health" -TimeoutSec 1 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Status "✅ Backend started successfully (Job ID: $($backendJob.Id))" "Green"
                return $true
            }
        }
        catch {
            # Continue waiting
        }
        Start-Sleep -Seconds 1
    }
    
    Write-Status "❌ Backend failed to start" "Red"
    return $false
}

# Function to start frontend
function Start-Frontend {
    Write-Status "⚛️  Starting Next.js frontend..." "Blue"
    
    Set-Location $FrontendDir
    
    # Start the frontend
    $frontendJob = Start-Job -ScriptBlock {
        param($FrontendDir)
        Set-Location $FrontendDir
        npm run dev
    } -ArgumentList (Resolve-Path $FrontendDir)
    
    $frontendJob.Id | Out-File -FilePath "..\$PidFile.frontend" -Encoding ASCII
    
    Set-Location ..
    
    # Wait for frontend to start
    Write-Status "Waiting for frontend to start..." "Yellow"
    for ($i = 1; $i -le 30; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$FrontendPort" -TimeoutSec 1 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Status "✅ Frontend started successfully (Job ID: $($frontendJob.Id))" "Green"
                
                # Open frontend in default browser (if enabled)
                if ($OpenBrowser) {
                    Write-Status "🌐 Opening frontend in default browser..." "Blue"
                    try {
                        Start-Process "http://localhost:$FrontendPort"
                    }
                    catch {
                        Write-Status "⚠️  Could not open browser automatically. Please open http://localhost:$FrontendPort manually" "Yellow"
                    }
                } else {
                    Write-Status "💡 Frontend ready at http://localhost:$FrontendPort" "Cyan"
                }
                
                return $true
            }
        }
        catch {
            # Continue waiting
        }
        Start-Sleep -Seconds 1
    }
    
    Write-Status "❌ Frontend failed to start" "Red"
    return $false
}

# Function to cleanup processes
function Stop-Services {
    Write-Status "🧹 Cleaning up processes..." "Yellow"
    
    # Stop backend job
    if (Test-Path "$PidFile.backend") {
        $backendJobId = Get-Content "$PidFile.backend"
        $backendJob = Get-Job -Id $backendJobId -ErrorAction SilentlyContinue
        if ($backendJob) {
            Write-Status "Stopping backend (Job ID: $backendJobId)..." "Yellow"
            Stop-Job -Id $backendJobId -ErrorAction SilentlyContinue
            Remove-Job -Id $backendJobId -ErrorAction SilentlyContinue
        }
        Remove-Item "$PidFile.backend" -ErrorAction SilentlyContinue
    }
    
    # Stop frontend job
    if (Test-Path "$PidFile.frontend") {
        $frontendJobId = Get-Content "$PidFile.frontend"
        $frontendJob = Get-Job -Id $frontendJobId -ErrorAction SilentlyContinue
        if ($frontendJob) {
            Write-Status "Stopping frontend (Job ID: $frontendJobId)..." "Yellow"
            Stop-Job -Id $frontendJobId -ErrorAction SilentlyContinue
            Remove-Job -Id $frontendJobId -ErrorAction SilentlyContinue
        }
        Remove-Item "$PidFile.frontend" -ErrorAction SilentlyContinue
    }
    
    # Kill any remaining processes on our ports
    Stop-Port $BackendPort
    Stop-Port $FrontendPort
    
    Write-Status "✅ Cleanup completed" "Green"
}

# Function to show status
function Show-Status {
    Write-Status "📊 Service Status:" "Blue"
    
    # Check backend
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$BackendPort/health" -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Status "✅ Backend: Running on port $BackendPort" "Green"
        } else {
            Write-Status "❌ Backend: Not running" "Red"
        }
    }
    catch {
        Write-Status "❌ Backend: Not running" "Red"
    }
    
    # Check frontend
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$FrontendPort" -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Status "✅ Frontend: Running on port $FrontendPort" "Green"
        } else {
            Write-Status "❌ Frontend: Not running" "Red"
        }
    }
    catch {
        Write-Status "❌ Frontend: Not running" "Red"
    }
}

# Function to restart services
function Restart-Services {
    Write-Status "🔄 Restarting services..." "Yellow"
    Stop-Services
    Start-Sleep -Seconds 2
    Start-Backend
    Start-Frontend
    Write-Status "✅ Services restarted" "Green"
}

# Function to show help
function Show-Help {
    Write-Host "Usage: .\dev.ps1 [COMMAND] [OPTIONS]" -ForegroundColor White
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Cyan
    Write-Host "  start     Start both frontend and backend (default)" -ForegroundColor Green
    Write-Host "  stop      Stop all services" -ForegroundColor Green
    Write-Host "  restart   Restart all services" -ForegroundColor Green
    Write-Host "  status    Show service status" -ForegroundColor Green
    Write-Host "  clean     Clean up processes and ports" -ForegroundColor Green
    Write-Host "  help      Show this help message" -ForegroundColor Green
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  -NoBrowser    Don't open browser automatically" -ForegroundColor Green
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\dev.ps1                    # Start both services with browser" -ForegroundColor White
    Write-Host "  .\dev.ps1 start              # Start both services with browser" -ForegroundColor White
    Write-Host "  .\dev.ps1 start -NoBrowser  # Start services without opening browser" -ForegroundColor White
    Write-Host "  .\dev.ps1 status             # Check service status" -ForegroundColor White
    Write-Host "  .\dev.ps1 stop               # Stop all services" -ForegroundColor White
}

# Main script logic
switch ($Command.ToLower()) {
    "start" {
        Write-Header
        
        # Check if ports are already in use
        if (Test-Port $BackendPort) {
            Write-Status "⚠️  Port $BackendPort is already in use" "Yellow"
            $response = Read-Host "Kill existing process? (y/N)"
            if ($response -eq "y" -or $response -eq "Y") {
                Stop-Port $BackendPort
            } else {
                Write-Status "❌ Cannot start backend on port $BackendPort" "Red"
                exit 1
            }
        }
        
        if (Test-Port $FrontendPort) {
            Write-Status "⚠️  Port $FrontendPort is already in use" "Yellow"
            $response = Read-Host "Kill existing process? (y/N)"
            if ($response -eq "y" -or $response -eq "Y") {
                Stop-Port $FrontendPort
            } else {
                Write-Status "❌ Cannot start frontend on port $FrontendPort" "Red"
                exit 1
            }
        }
        
        # Check and setup environments
        Test-PythonEnv
        Test-NodeModules
        Install-PythonDeps
        
        # Start services
        Start-Backend
        Start-Frontend
        
        Write-Status "🎉 All services started successfully!" "Green"
        Write-Status "Press Ctrl+C to stop all services" "Cyan"
        
        # Keep script running
        try {
            while ($true) {
                Start-Sleep -Seconds 1
            }
        }
        catch {
            Stop-Services
        }
    }
    
    "stop" {
        Stop-Services
    }
    
    "restart" {
        Restart-Services
    }
    
    "status" {
        Show-Status
    }
    
    "clean" {
        Stop-Services
    }
    
    "help" {
        Show-Help
    }
    
    default {
        Write-Status "❌ Unknown command: $Command" "Red"
        Show-Help
        exit 1
    }
}
