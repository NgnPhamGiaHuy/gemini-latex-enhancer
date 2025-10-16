#!/bin/bash

# =============================================================================
# Gemini LaTeX Enhancer - Development Script for macOS
# =============================================================================
# This script runs both the frontend (Next.js) and backend (FastAPI) 
# simultaneously with proper process management, logging, and cleanup.
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
FRONTEND_PORT=3000
BACKEND_PORT=8000
FRONTEND_DIR="frontend"
BACKEND_DIR="backend"
LOG_DIR="logs"
PID_FILE="dev.pid"
OPEN_BROWSER=true  # Set to false to disable auto-opening browser

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    local timestamp=$(date '+%H:%M:%S')
    echo -e "${color}[$timestamp] $message${NC}"
}

print_header() {
    echo -e "${WHITE}=============================================================================${NC}"
    echo -e "${WHITE}🚀 Gemini LaTeX Enhancer - Development Environment${NC}"
    echo -e "${WHITE}=============================================================================${NC}"
    echo -e "${CYAN}Frontend: http://localhost:$FRONTEND_PORT${NC}"
    echo -e "${CYAN}Backend:  http://localhost:$BACKEND_PORT${NC}"
    echo -e "${CYAN}Health:   http://localhost:$BACKEND_PORT/health${NC}"
    echo -e "${WHITE}=============================================================================${NC}"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local pids=$(lsof -ti :$port 2>/dev/null || true)
    if [ ! -z "$pids" ]; then
        print_status $YELLOW "Killing processes on port $port..."
        echo $pids | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
}

# Function to check if Python virtual environment exists
check_python_env() {
    if [ ! -d "$BACKEND_DIR/venv" ]; then
        print_status $RED "❌ Python virtual environment not found!"
        print_status $YELLOW "Creating virtual environment..."
        cd "$BACKEND_DIR"
        python3 -m venv venv
        cd ..
        print_status $GREEN "✅ Virtual environment created"
    fi
}

# Function to check if Node modules exist
check_node_modules() {
    if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
        print_status $RED "❌ Node modules not found!"
        print_status $YELLOW "Installing dependencies..."
        cd "$FRONTEND_DIR"
        npm install
        cd ..
        print_status $GREEN "✅ Dependencies installed"
    fi
}

# Function to install Python dependencies
install_python_deps() {
    print_status $YELLOW "Installing Python dependencies..."
    cd "$BACKEND_DIR"
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    print_status $GREEN "✅ Python dependencies installed"
}

# Function to start backend
start_backend() {
    print_status $BLUE "🐍 Starting FastAPI backend..."
    
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # Check if GEMINI_API_KEY is set
    if [ -z "$GEMINI_API_KEY" ]; then
        if [ -f "../.env" ]; then
            print_status $YELLOW "⚠️  GEMINI_API_KEY not found in environment variables"
            print_status $CYAN "💡 Found .env file in root directory - the backend will load it automatically"
        else
            print_status $YELLOW "⚠️  GEMINI_API_KEY not set. Please set it in your environment or create .env file in root directory"
        fi
    else
        print_status $GREEN "✅ GEMINI_API_KEY found in environment"
    fi
    
    # Start the backend with proper logging
    nohup python -m uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload \
        > "../$LOG_DIR/backend.log" 2>&1 &
    
    BACKEND_PID=$!
    echo $BACKEND_PID > "../$PID_FILE.backend"
    
    cd ..
    
    # Wait for backend to start
    print_status $YELLOW "Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:$BACKEND_PORT/health >/dev/null 2>&1; then
            print_status $GREEN "✅ Backend started successfully (PID: $BACKEND_PID)"
            return 0
        fi
        sleep 1
    done
    
    print_status $RED "❌ Backend failed to start"
    return 1
}

# Function to start frontend
start_frontend() {
    print_status $BLUE "⚛️  Starting Next.js frontend..."
    
    cd "$FRONTEND_DIR"
    
    # Start the frontend with proper logging
    nohup npm run dev \
        > "../$LOG_DIR/frontend.log" 2>&1 &
    
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "../$PID_FILE.frontend"
    
    cd ..
    
    # Wait for frontend to start
    print_status $YELLOW "Waiting for frontend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
            print_status $GREEN "✅ Frontend started successfully (PID: $FRONTEND_PID)"
            
            # Open frontend in default browser (if enabled)
            if [ "$OPEN_BROWSER" = "true" ]; then
                print_status $BLUE "🌐 Opening frontend in default browser..."
                if command -v open >/dev/null 2>&1; then
                    # macOS
                    open "http://localhost:$FRONTEND_PORT"
                elif command -v xdg-open >/dev/null 2>&1; then
                    # Linux
                    xdg-open "http://localhost:$FRONTEND_PORT"
                elif command -v start >/dev/null 2>&1; then
                    # Windows (if running in Git Bash)
                    start "http://localhost:$FRONTEND_PORT"
                else
                    print_status $YELLOW "⚠️  Could not detect browser command. Please open http://localhost:$FRONTEND_PORT manually"
                fi
            else
                print_status $CYAN "💡 Frontend ready at http://localhost:$FRONTEND_PORT"
            fi
            
            return 0
        fi
        sleep 1
    done
    
    print_status $RED "❌ Frontend failed to start"
    return 1
}

# Function to cleanup processes
cleanup() {
    print_status $YELLOW "🧹 Cleaning up processes..."
    
    # Kill backend
    if [ -f "$PID_FILE.backend" ]; then
        BACKEND_PID=$(cat "$PID_FILE.backend")
        if kill -0 $BACKEND_PID 2>/dev/null; then
            print_status $YELLOW "Stopping backend (PID: $BACKEND_PID)..."
            kill $BACKEND_PID 2>/dev/null || true
        fi
        rm -f "$PID_FILE.backend"
    fi
    
    # Kill frontend
    if [ -f "$PID_FILE.frontend" ]; then
        FRONTEND_PID=$(cat "$PID_FILE.frontend")
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            print_status $YELLOW "Stopping frontend (PID: $FRONTEND_PID)..."
            kill $FRONTEND_PID 2>/dev/null || true
        fi
        rm -f "$PID_FILE.frontend"
    fi
    
    # Kill any remaining processes on our ports
    kill_port $BACKEND_PORT
    kill_port $FRONTEND_PORT
    
    print_status $GREEN "✅ Cleanup completed"
}

# Function to show logs
show_logs() {
    local service=$1
    if [ "$service" = "backend" ]; then
        print_status $BLUE "📋 Backend logs:"
        tail -f "$LOG_DIR/backend.log"
    elif [ "$service" = "frontend" ]; then
        print_status $BLUE "📋 Frontend logs:"
        tail -f "$LOG_DIR/frontend.log"
    else
        print_status $BLUE "📋 All logs:"
        tail -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log"
    fi
}

# Function to show status
show_status() {
    print_status $BLUE "📊 Service Status:"
    
    # Check backend
    if curl -s http://localhost:$BACKEND_PORT/health >/dev/null 2>&1; then
        print_status $GREEN "✅ Backend: Running on port $BACKEND_PORT"
    else
        print_status $RED "❌ Backend: Not running"
    fi
    
    # Check frontend
    if curl -s http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
        print_status $GREEN "✅ Frontend: Running on port $FRONTEND_PORT"
    else
        print_status $RED "❌ Frontend: Not running"
    fi
}

# Function to restart services
restart() {
    print_status $YELLOW "🔄 Restarting services..."
    cleanup
    sleep 2
    start_backend
    start_frontend
    print_status $GREEN "✅ Services restarted"
}

# Function to show help
show_help() {
    echo -e "${WHITE}Usage: $0 [COMMAND] [OPTIONS]${NC}"
    echo ""
    echo -e "${CYAN}Commands:${NC}"
    echo -e "  ${GREEN}start${NC}     Start both frontend and backend (default)"
    echo -e "  ${GREEN}stop${NC}      Stop all services"
    echo -e "  ${GREEN}restart${NC}   Restart all services"
    echo -e "  ${GREEN}status${NC}    Show service status"
    echo -e "  ${GREEN}logs${NC}      Show logs (backend|frontend|all)"
    echo -e "  ${GREEN}clean${NC}     Clean up processes and ports"
    echo -e "  ${GREEN}help${NC}      Show this help message"
    echo ""
    echo -e "${CYAN}Options:${NC}"
    echo -e "  ${GREEN}--browser${NC}     Open browser automatically (default)"
    echo -e "  ${GREEN}--no-browser${NC} Don't open browser automatically"
    echo ""
    echo -e "${CYAN}Examples:${NC}"
    echo -e "  $0                           # Start both services with browser"
    echo -e "  $0 start                     # Start both services with browser"
    echo -e "  $0 start --no-browser        # Start services without opening browser"
    echo -e "  $0 logs backend              # Show backend logs"
    echo -e "  $0 logs frontend             # Show frontend logs"
    echo -e "  $0 logs                      # Show all logs"
    echo -e "  $0 status                    # Check service status"
    echo -e "  $0 stop                      # Stop all services"
}

# Trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-browser)
            OPEN_BROWSER=false
            shift
            ;;
        --browser)
            OPEN_BROWSER=true
            shift
            ;;
        *)
            COMMAND="$1"
            shift
            ;;
    esac
done

# Main script logic
case "${COMMAND:-start}" in
    "start")
        print_header
        
        # Check if ports are already in use
        if check_port $BACKEND_PORT; then
            print_status $YELLOW "⚠️  Port $BACKEND_PORT is already in use"
            read -p "Kill existing process? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                kill_port $BACKEND_PORT
            else
                print_status $RED "❌ Cannot start backend on port $BACKEND_PORT"
                exit 1
            fi
        fi
        
        if check_port $FRONTEND_PORT; then
            print_status $YELLOW "⚠️  Port $FRONTEND_PORT is already in use"
            read -p "Kill existing process? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                kill_port $FRONTEND_PORT
            else
                print_status $RED "❌ Cannot start frontend on port $FRONTEND_PORT"
                exit 1
            fi
        fi
        
        # Check and setup environments
        check_python_env
        check_node_modules
        install_python_deps
        
        # Start services
        start_backend
        start_frontend
        
        print_status $GREEN "🎉 All services started successfully!"
        print_status $CYAN "Press Ctrl+C to stop all services"
        
        # Keep script running and show logs
        show_logs
        ;;
        
    "stop")
        cleanup
        ;;
        
    "restart")
        restart
        ;;
        
    "status")
        show_status
        ;;
        
    "logs")
        show_logs "${2:-all}"
        ;;
        
    "clean")
        cleanup
        ;;
        
    "help"|"-h"|"--help")
        show_help
        ;;
        
    *)
        print_status $RED "❌ Unknown command: $1"
        show_help
        exit 1
        ;;
esac
