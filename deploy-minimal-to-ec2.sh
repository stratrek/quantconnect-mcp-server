#!/bin/bash

# QuantConnect MCP MINIMAL Server EC2 Deployment Script
# Deploys the minimal version (8 tools only) to a NEW EC2 instance

set -e  # Exit on any error

# Configuration - UPDATE THESE FOR NEW INSTANCE
EC2_INSTANCE_IP="54.156.64.245"  # New minimal server instance
EC2_USER="ubuntu"
SSH_KEY_PATH="$HOME/.ssh/quantconnect-mcp-key.pem"
REPO_URL="https://github.com/stratrek/quantconnect-mcp-server.git"
DEPLOY_DIR="stratrek-quantconnect-mcp-server"
SERVICE_NAME="quantconnect-mcp-minimal.service"
BACKUP_DIR="quantconnect-mcp-minimal-backup-$(date +%Y%m%d-%H%M%S)"
SERVER_TYPE="MINIMAL"

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

echo "🚀 QuantConnect MCP MINIMAL Server EC2 Deployment"
echo "=================================================="
echo "🔒 This deploys ONLY 8 essential tools (88% reduction)"

# Check if IP is still placeholder
if [[ "$EC2_INSTANCE_IP" == "PLACEHOLDER_IP" ]]; then
    log_error "Please update EC2_INSTANCE_IP in this script with your new instance IP address"
    echo "Launch a new EC2 instance first, then update the IP in this script"
    exit 1
fi

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
log_info "Testing SSH connectivity to NEW EC2 instance..."
if ! run_remote "echo 'SSH connection successful'" > /dev/null 2>&1; then
    log_error "Cannot connect to NEW EC2 instance. Please check:"
    echo "  - New instance is running ($EC2_INSTANCE_IP)"
    echo "  - Security group allows SSH (port 22)"
    echo "  - SSH key is correct"
    exit 1
fi
log_success "SSH connectivity confirmed to NEW instance"

# Check if we're in a git repository
if ! git status > /dev/null 2>&1; then
    log_error "Not in a git repository. Please run this script from the repository root."
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git diff --name-only) || -n $(git diff --cached --name-only) ]]; then
    log_warning "You have uncommitted changes. Consider committing them first."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

log_success "Local validation completed"

# Phase 2: Remote Environment Setup
log_info "Phase 2: Remote Environment Setup (NEW Instance)"

# Check if this is a fresh instance
log_info "Checking if this is a fresh EC2 instance..."
run_remote "
    set -e
    echo 'System information:'
    uname -a
    echo 'Python version:'
    python3 --version

    # Check if this instance already has a deployment
    if [[ -d quantconnect-mcp-deploy ]] || [[ -d $DEPLOY_DIR ]]; then
        echo 'WARNING: Found existing deployment directories'
        ls -la | grep quantconnect || true
    else
        echo 'Fresh instance - no existing deployments found'
    fi
"

# Install uv package manager
log_info "Installing uv package manager on NEW instance..."
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
            echo 'uv installation failed'
            exit 1
        fi
    fi
"
log_success "uv package manager ready on NEW instance"

# Phase 3: Code Deployment
log_info "Phase 3: MINIMAL Server Code Deployment"

# Clone the repository
log_info "Cloning repository to NEW EC2 instance..."
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
log_success "Repository cloned to NEW instance"

# Install dependencies
log_info "Installing dependencies on NEW instance..."
run_remote "
    set -e
    cd $DEPLOY_DIR

    # Ensure uv is in PATH
    export PATH=\"\$HOME/.local/bin:\$PATH\"

    echo 'Installing dependencies with uv...'
    uv sync

    echo 'Dependencies installed successfully'
"
log_success "Dependencies installed on NEW instance"

# Phase 4: MINIMAL Server Configuration
log_info "Phase 4: MINIMAL Server Configuration"

# Create environment file for minimal server
log_info "Creating environment configuration for MINIMAL server..."
run_remote "
    set -e
    cd $DEPLOY_DIR

    # Create .env file for minimal server (will need manual configuration)
    cat > .env << 'EOF'
# QuantConnect MCP MINIMAL Server Environment
# Only 8 tools exposed for security

# Transport Configuration
MCP_TRANSPORT=http
MCP_HOST=0.0.0.0
MCP_PORT=8001

# QuantConnect API Credentials
# TODO: Add your credentials here
# QUANTCONNECT_USER_ID=your_user_id_here
# QUANTCONNECT_API_TOKEN=your_api_token_here

# Optional Agent Name
AGENT_NAME=MCP-Minimal-Server
EOF

    echo 'Environment template created. Manual configuration required.'
    echo 'You will need to add your QuantConnect credentials.'
"

# Update systemd service configuration for MINIMAL server
log_info "Creating systemd service for MINIMAL server..."
run_remote "
    set -e

    # Create new systemd service file for minimal server
    sudo tee /etc/systemd/system/$SERVICE_NAME > /dev/null << 'EOF'
[Unit]
Description=QuantConnect MCP MINIMAL Server (8 tools only)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/$DEPLOY_DIR
Environment=PATH=/home/ubuntu/.local/bin:/home/ubuntu/$DEPLOY_DIR/.venv/bin
EnvironmentFile=/home/ubuntu/$DEPLOY_DIR/.env
ExecStart=/home/ubuntu/.local/bin/uv run src/main_minimal.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    echo 'Systemd service file created for MINIMAL server'

    # Reload systemd
    sudo systemctl daemon-reload
    echo 'Systemd reloaded'
"
log_success "MINIMAL server service configured"

# Phase 5: Manual Configuration Pause
echo ""
log_warning "MANUAL CONFIGURATION REQUIRED"
echo "=============================================="
echo "Before starting the service, you need to:"
echo "1. Add your QuantConnect credentials to /home/ubuntu/$DEPLOY_DIR/.env"
echo ""
echo "Connect to the instance and edit the .env file:"
echo "ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_INSTANCE_IP"
echo "cd $DEPLOY_DIR"
echo "nano .env"
echo ""
echo "Add these lines:"
echo "QUANTCONNECT_USER_ID=your_actual_user_id"
echo "QUANTCONNECT_API_TOKEN=your_actual_api_token"
echo ""
read -p "Press Enter after you've configured the credentials..."

# Phase 6: Service Management
log_info "Phase 6: MINIMAL Server Service Management"

# Start the minimal service
log_info "Starting MINIMAL server service..."
run_remote "
    set -e

    echo 'Enabling MINIMAL service...'
    sudo systemctl enable $SERVICE_NAME

    echo 'Starting MINIMAL service...'
    sudo systemctl start $SERVICE_NAME

    # Wait for service to start
    sleep 5

    echo 'MINIMAL service status:'
    sudo systemctl status $SERVICE_NAME --no-pager || true
"
log_success "MINIMAL server service started"

# Phase 7: Verification & Testing
log_info "Phase 7: MINIMAL Server Verification"

# Check service health
log_info "Performing health checks on MINIMAL server..."
run_remote "
    set -e

    # Check if service is active
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo 'MINIMAL service is active ✅'
    else
        echo 'MINIMAL service is not active ❌'
        echo 'Service status:'
        sudo systemctl status $SERVICE_NAME --no-pager
        exit 1
    fi

    # Get the configured port
    MCP_PORT=\$(grep '^MCP_PORT=' .env | cut -d'=' -f2 || echo '8001')
    echo \"MINIMAL server port: \$MCP_PORT\"

    # Check if port is listening
    sleep 3
    if netstat -tlnp 2>/dev/null | grep -q \":\$MCP_PORT\"; then
        echo \"MINIMAL server listening on port \$MCP_PORT ✅\"
    else
        echo \"MINIMAL server not listening on port \$MCP_PORT ❌\"
        echo 'Open ports:'
        netstat -tlnp 2>/dev/null | grep LISTEN || true
        exit 1
    fi
"

# Test MCP endpoint
log_info "Testing MINIMAL MCP endpoint..."
HTTP_RESPONSE=$(curl -s -H "Accept: text/event-stream" "http://$EC2_INSTANCE_IP:8001/mcp" || echo "CONNECTION_FAILED")

if [[ "$HTTP_RESPONSE" == "CONNECTION_FAILED" ]]; then
    log_error "Cannot connect to MINIMAL MCP endpoint"
    run_remote "
        echo 'MINIMAL service logs (last 20 lines):'
        sudo journalctl -u $SERVICE_NAME -n 20 --no-pager
    "
    exit 1
elif [[ "$HTTP_RESPONSE" == *"Missing session ID"* ]]; then
    log_success "MINIMAL MCP endpoint responding correctly"
else
    log_warning "Unexpected response: $HTTP_RESPONSE"
fi

# Test tools list
log_info "Testing tools list (should show only 8 tools)..."
TOOLS_TEST=$(curl -s -X POST "http://$EC2_INSTANCE_IP:8001/mcp" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' || echo "FAILED")

if [[ "$TOOLS_TEST" == *"read_file"* ]] && [[ "$TOOLS_TEST" == *"update_file_contents"* ]]; then
    log_success "Tools endpoint responding - essential tools detected"
else
    log_warning "Tools list test inconclusive"
fi

# Show final status
echo ""
echo "🎉 MINIMAL Server Deployment Completed!"
echo "========================================"
echo ""
log_success "QuantConnect MCP MINIMAL server is running on NEW instance"
echo "📍 Instance: $EC2_INSTANCE_IP (NEW)"
echo "🌐 Endpoint: http://$EC2_INSTANCE_IP:8001/mcp"
echo "🔒 Security: Only 8 tools exposed (88% reduction)"
echo "📁 Deploy Dir: /home/ubuntu/$DEPLOY_DIR"
echo ""
echo "🛠️  Available Tools:"
echo "  1. read_file"
echo "  2. update_file_contents"
echo "  3. create_compile"
echo "  4. read_compile"
echo "  5. create_backtest_brief"
echo "  6. read_backtest_brief"
echo "  7. read_backtest_statistics"
echo "  8. search_quantconnect"
echo ""
echo "Management Commands:"
echo "  View logs:    ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_INSTANCE_IP 'sudo journalctl -u $SERVICE_NAME -f'"
echo "  Service status: ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_INSTANCE_IP 'sudo systemctl status $SERVICE_NAME'"
echo "  Restart:      ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_INSTANCE_IP 'sudo systemctl restart $SERVICE_NAME'"
echo ""
log_info "Test with: curl -X POST http://$EC2_INSTANCE_IP:8001/mcp -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\"}'"