#!/bin/bash

# QuantConnect MCP Server EC2 Deployment Script
# Deploys your enhanced QuantConnect MCP server fork to existing EC2 instance

set -e  # Exit on any error

# Configuration
EC2_INSTANCE_IP="100.24.29.103"
EC2_USER="ubuntu"
SSH_KEY_PATH="$HOME/.ssh/quantconnect-mcp-key.pem"
REPO_URL="https://github.com/stratrek/quantconnect-mcp-server.git"
DEPLOY_DIR="stratrek-quantconnect-mcp-server"
SERVICE_NAME="quantconnect-mcp.service"
BACKUP_DIR="quantconnect-mcp-deploy-backup-$(date +%Y%m%d-%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to run commands on EC2 instance
run_remote() {
    ssh -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_INSTANCE_IP" "$@"
}

# Function to copy files to EC2 instance
copy_to_remote() {
    scp -i "$SSH_KEY_PATH" -o StrictHostKeyChecking=no "$@"
}

echo "🚀 QuantConnect MCP Server EC2 Deployment"
echo "=============================================="

# Phase 1: Local Validation
log_info "Phase 1: Local Validation"

# Check if SSH key exists
if [[ ! -f "$SSH_KEY_PATH" ]]; then
    log_error "SSH key not found: $SSH_KEY_PATH"
    echo "Please ensure the SSH key exists and has correct permissions (400)"
    exit 1
fi

# Check SSH key permissions
KEY_PERMS=$(stat -c "%a" "$SSH_KEY_PATH")
if [[ "$KEY_PERMS" != "400" ]]; then
    log_warning "SSH key permissions are $KEY_PERMS, should be 400. Fixing..."
    chmod 400 "$SSH_KEY_PATH"
    log_success "SSH key permissions fixed"
fi

# Test SSH connectivity
log_info "Testing SSH connectivity to EC2 instance..."
if ! run_remote "echo 'SSH connection successful'" > /dev/null 2>&1; then
    log_error "Cannot connect to EC2 instance. Please check:"
    echo "  - Instance is running"
    echo "  - Security group allows SSH (port 22)"
    echo "  - SSH key is correct"
    exit 1
fi
log_success "SSH connectivity confirmed"

# Check if we're in a git repository
if ! git status > /dev/null 2>&1; then
    log_error "Not in a git repository. Please run this script from the repository root."
    exit 1
fi

# Check for uncommitted changes to tracked files only
if [[ -n $(git diff --name-only) || -n $(git diff --cached --name-only) ]]; then
    log_warning "You have uncommitted changes to tracked files. Consider committing them first."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

log_success "Local validation completed"

# Phase 2: Remote Environment Setup
log_info "Phase 2: Remote Environment Setup"

# Check current service status and create backup
log_info "Checking current deployment and creating backup..."
run_remote "
    set -e
    echo 'Current service status:'
    sudo systemctl status $SERVICE_NAME --no-pager || true
    
    # Create backup of current deployment if it exists
    if [[ -d quantconnect-mcp-deploy ]]; then
        echo 'Creating backup of current deployment...'
        cp -r quantconnect-mcp-deploy $BACKUP_DIR
        echo 'Backup created: $BACKUP_DIR'
    fi
    
    # Check Python version
    echo 'Python version:'
    python3 --version
"

# Install uv package manager
log_info "Installing uv package manager..."
run_remote "
    set -e
    
    # Check if uv is already installed
    if command -v uv > /dev/null 2>&1; then
        echo 'uv is already installed:'
        uv --version
    else
        echo 'Installing uv...'
        curl -LsSf https://astral.sh/uv/install.sh | sh
        
        # Source the environment to make uv available
        export PATH=\"\$HOME/.local/bin:\$PATH\"
        
        # Verify installation
        if command -v uv > /dev/null 2>&1; then
            echo 'uv installation successful:'
            uv --version
        else
            echo 'uv installation failed, will fall back to pip'
            exit 1
        fi
    fi
"

if [ $? -eq 0 ]; then
    log_success "uv package manager installed"
    USE_UV=true
else
    log_warning "uv installation failed, will use pip as fallback"
    USE_UV=false
fi

# Phase 3: Code Deployment
log_info "Phase 3: Code Deployment"

# Clone the repository
log_info "Cloning repository to EC2 instance..."
run_remote "
    set -e
    
    # Remove existing deployment directory if it exists
    if [[ -d $DEPLOY_DIR ]]; then
        echo 'Removing existing deployment directory...'
        rm -rf $DEPLOY_DIR
    fi
    
    # Clone the repository
    echo 'Cloning repository...'
    git clone $REPO_URL $DEPLOY_DIR
    
    cd $DEPLOY_DIR
    echo 'Repository cloned successfully. Latest commit:'
    git log --oneline -n 1
"

log_success "Repository cloned successfully"

# Install dependencies
log_info "Installing dependencies..."
if [ "$USE_UV" = true ]; then
    run_remote "
        set -e
        cd $DEPLOY_DIR
        
        # Ensure uv is in PATH
        export PATH=\"\$HOME/.local/bin:\$PATH\"
        
        echo 'Installing dependencies with uv...'
        uv sync
        
        echo 'Dependencies installed successfully'
    "
    log_success "Dependencies installed with uv"
else
    # Fallback to pip
    run_remote "
        set -e
        cd $DEPLOY_DIR
        
        echo 'Creating virtual environment with Python venv...'
        python3 -m venv venv
        source venv/bin/activate
        
        echo 'Upgrading pip...'
        pip install --upgrade pip
        
        echo 'Installing dependencies...'
        if [[ -f pyproject.toml ]]; then
            pip install .
        else
            pip install -r requirements.txt
        fi
        
        echo 'Dependencies installed successfully'
    "
    log_success "Dependencies installed with pip"
fi

# Phase 4: Service Configuration
log_info "Phase 4: Service Configuration"

# Copy existing environment variables
log_info "Copying existing environment configuration..."
run_remote "
    set -e
    
    # Copy .env file from backup if it exists
    if [[ -f quantconnect-mcp-deploy/.env ]]; then
        echo 'Copying existing environment configuration...'
        cp quantconnect-mcp-deploy/.env $DEPLOY_DIR/
        echo 'Environment configuration copied'
        
        # Show environment variables (without sensitive values)
        echo 'Current environment variables:'
        sed 's/=.*/=***/' $DEPLOY_DIR/.env
    else
        echo 'No existing .env file found. You will need to configure environment variables manually.'
    fi
"

# Update systemd service configuration
log_info "Updating systemd service configuration..."
run_remote "
    set -e
    
    # Create new systemd service file
    sudo tee /etc/systemd/system/$SERVICE_NAME > /dev/null << 'EOF'
[Unit]
Description=QuantConnect MCP Server (Enhanced Fork)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/$DEPLOY_DIR
Environment=PATH=/home/ubuntu/$DEPLOY_DIR/.venv/bin
EnvironmentFile=/home/ubuntu/$DEPLOY_DIR/.env
ExecStart=/home/ubuntu/$DEPLOY_DIR/.venv/bin/python src/main.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    echo 'Systemd service file updated'
    
    # Reload systemd
    sudo systemctl daemon-reload
    echo 'Systemd reloaded'
"

log_success "Service configuration updated"

# Phase 5: Service Management
log_info "Phase 5: Service Management"

# Stop current service
log_info "Stopping current service..."
run_remote "
    set -e
    
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo 'Stopping current service...'
        sudo systemctl stop $SERVICE_NAME
        sleep 3
        echo 'Service stopped'
    else
        echo 'Service was not running'
    fi
"

# Start service with new code
log_info "Starting service with new code..."
run_remote "
    set -e
    
    echo 'Enabling service...'
    sudo systemctl enable $SERVICE_NAME
    
    echo 'Starting service...'
    sudo systemctl start $SERVICE_NAME
    
    # Wait for service to start
    sleep 5
    
    echo 'Service status:'
    sudo systemctl status $SERVICE_NAME --no-pager || true
"

log_success "Service restarted with new code"

# Phase 6: Verification & Testing
log_info "Phase 6: Verification & Testing"

# Check service health
log_info "Performing health checks..."
run_remote "
    set -e
    
    # Check if service is active
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo 'Service is active ✅'
    else
        echo 'Service is not active ❌'
        echo 'Service status:'
        sudo systemctl status $SERVICE_NAME --no-pager
        exit 1
    fi
    
    # Get the configured port from .env file
    if [[ -f $DEPLOY_DIR/.env ]]; then
        MCP_PORT=\$(grep '^MCP_PORT=' $DEPLOY_DIR/.env | cut -d'=' -f2)
        echo \"Configured port: \$MCP_PORT\"
    else
        MCP_PORT=8000
        echo \"Default port: \$MCP_PORT\"
    fi
    
    # Check if port is listening
    sleep 3
    if netstat -tlnp 2>/dev/null | grep -q \":\$MCP_PORT\"; then
        echo \"Service is listening on port \$MCP_PORT ✅\"
    else
        echo \"Service is not listening on expected port \$MCP_PORT ❌\"
        echo 'Open ports:'
        netstat -tlnp 2>/dev/null | grep LISTEN || true
        exit 1
    fi
"

# Test MCP endpoint
log_info "Testing MCP endpoint..."

# Get the configured port from the remote .env file  
REMOTE_PORT=$(run_remote "grep '^MCP_PORT=' $DEPLOY_DIR/.env | cut -d'=' -f2" 2>/dev/null || echo "8000")

HTTP_RESPONSE=$(curl -s -H "Accept: text/event-stream" "http://$EC2_INSTANCE_IP:$REMOTE_PORT/mcp" || echo "CONNECTION_FAILED")

if [[ "$HTTP_RESPONSE" == "CONNECTION_FAILED" ]]; then
    log_error "Cannot connect to MCP endpoint"
    run_remote "
        echo 'Service logs (last 20 lines):'
        sudo journalctl -u $SERVICE_NAME -n 20 --no-pager
    "
    exit 1
elif [[ "$HTTP_RESPONSE" == *"Missing session ID"* ]]; then
    log_success "MCP endpoint is responding correctly (Missing session ID is expected)"
else
    log_warning "Unexpected response from MCP endpoint: $HTTP_RESPONSE"
fi

# Show final status
echo ""
echo "🎉 Deployment Completed Successfully!"
echo "======================================"
echo ""
log_success "Enhanced QuantConnect MCP server is running"
echo "📍 Instance: $EC2_INSTANCE_IP"
echo "🌐 Endpoint: http://$EC2_INSTANCE_IP:$REMOTE_PORT/mcp"
echo "📁 Deploy Dir: /home/ubuntu/$DEPLOY_DIR"
echo "💾 Backup: /home/ubuntu/$BACKUP_DIR"
echo ""
echo "Management Commands:"
echo "  View logs:    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_INSTANCE_IP 'sudo journalctl -u $SERVICE_NAME -f'"
echo "  Service status: ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_INSTANCE_IP 'sudo systemctl status $SERVICE_NAME'"
echo "  Restart:      ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_INSTANCE_IP 'sudo systemctl restart $SERVICE_NAME'"
echo ""

log_info "Test the deployment with:"
echo "curl -X POST http://$EC2_INSTANCE_IP:$REMOTE_PORT/mcp \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\"}'"