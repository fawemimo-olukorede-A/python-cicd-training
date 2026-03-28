#!/bin/bash
# =============================================================================
# Azure VM Setup Script for Flask Application
# =============================================================================
# Run this script on your Azure VMs (both staging and production)
# to prepare them for deployments.
#
# Usage: sudo bash vm-setup.sh
# =============================================================================

set -e

echo "🔧 Setting up Azure VM for Flask deployments..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
echo "🐍 Installing Python..."
sudo apt-get install -y python3 python3-pip python3-venv

# Install system dependencies
echo "📚 Installing system dependencies..."
sudo apt-get install -y nginx curl git

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/flask-app
sudo chown $USER:$USER /opt/flask-app

# Create systemd service for Flask app
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/flask-app.service > /dev/null << 'EOF'
[Unit]
Description=Flask Application
After=network.target

[Service]
User=azureuser
Group=azureuser
WorkingDirectory=/opt/flask-app
Environment="PATH=/opt/flask-app/venv/bin"
Environment="FLASK_ENV=staging"
ExecStart=/opt/flask-app/venv/bin/gunicorn -w 4 -b 0.0.0.0:${APP_PORT:-5000} app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload
sudo systemctl enable flask-app

# Configure firewall (allow port 5000)
echo "🔥 Configuring firewall..."
sudo ufw allow ${APP_PORT:-5000}/tcp || true
sudo ufw allow 22/tcp || true
sudo ufw allow 80/tcp || true

# Create log directory
sudo mkdir -p /var/log/flask-app
sudo chown $USER:$USER /var/log/flask-app

echo ""
echo "✅ VM Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Add your SSH public key to ~/.ssh/authorized_keys"
echo "2. Note down the VM's IP address for GitHub Secrets"
echo "3. Test SSH access: ssh azureuser@<VM-IP>"
echo ""
echo "After deployment, your app will be available at:"
echo "  http://<VM-IP>:${APP_PORT:-5000}"
