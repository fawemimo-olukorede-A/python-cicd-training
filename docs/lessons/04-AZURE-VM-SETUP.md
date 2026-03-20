# Module 4: Azure VM Setup for Deployments

## Overview

In this module, we'll set up two Azure VMs:
1. **Staging VM** - For testing before production
2. **Production VM** - For live users

```
┌─────────────────────────────────────────────────────────────────┐
│                        AZURE CLOUD                               │
│                                                                  │
│    ┌─────────────────┐           ┌─────────────────┐            │
│    │   STAGING VM    │           │  PRODUCTION VM  │            │
│    │                 │           │                 │            │
│    │  IP: 20.x.x.x   │           │  IP: 20.y.y.y   │            │
│    │  Port: 5000     │           │  Port: 5000     │            │
│    │                 │           │                 │            │
│    │  FLASK_ENV=     │           │  FLASK_ENV=     │            │
│    │  staging        │           │  production     │            │
│    └────────┬────────┘           └────────┬────────┘            │
│             │                             │                      │
│             │      SSH (Port 22)          │                      │
│             └──────────┬──────────────────┘                      │
│                        │                                         │
└────────────────────────┼─────────────────────────────────────────┘
                         │
                    GitHub Actions
                    (Deployment)
```

---

## Step 1: Create Azure VMs

### Using Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **Create a resource** → **Virtual Machine**
3. Configure:

| Setting | Staging VM | Production VM |
|---------|------------|---------------|
| Name | `flask-staging-vm` | `flask-prod-vm` |
| Region | Your nearest region | Same region |
| Image | Ubuntu Server 22.04 LTS | Ubuntu Server 22.04 LTS |
| Size | Standard_B1s (1 vCPU, 1GB) | Standard_B2s (2 vCPU, 4GB) |
| Authentication | SSH public key | SSH public key |
| Username | `azureuser` | `azureuser` |

4. **Networking**: Allow ports 22 (SSH), 80 (HTTP), 5000 (Flask)

### Using Azure CLI (Alternative)

```bash
# Login to Azure
az login

# Create resource group
az group create --name flask-cicd-rg --location eastus

# Create Staging VM
az vm create \
  --resource-group flask-cicd-rg \
  --name flask-staging-vm \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Create Production VM
az vm create \
  --resource-group flask-cicd-rg \
  --name flask-prod-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Open port 5000 on both VMs
az vm open-port --resource-group flask-cicd-rg --name flask-staging-vm --port 5000
az vm open-port --resource-group flask-cicd-rg --name flask-prod-vm --port 5000
```

---

## Step 2: Get VM IP Addresses

```bash
# Get Staging VM IP
az vm show -d -g flask-cicd-rg -n flask-staging-vm --query publicIps -o tsv

# Get Production VM IP
az vm show -d -g flask-cicd-rg -n flask-prod-vm --query publicIps -o tsv
```

**Note these IPs! You'll need them for GitHub Secrets.**

---

## Step 3: SSH into VMs and Run Setup

### Connect to Staging VM
```bash
ssh azureuser@<STAGING_VM_IP>
```

### Run Setup Script

Once connected, run these commands:

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3 python3-pip python3-venv

# Create application directory
sudo mkdir -p /opt/flask-app
sudo chown azureuser:azureuser /opt/flask-app

# Create systemd service
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
ExecStart=/opt/flask-app/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
sudo systemctl daemon-reload
sudo systemctl enable flask-app

echo "✅ VM Setup Complete!"
```

**Repeat for Production VM** (change `FLASK_ENV=production`).

---

## Step 4: Generate SSH Keys for GitHub Actions

On your **local machine** (not the VM):

```bash
# Generate a new SSH key pair
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github-deploy-key -N ""

# Display the private key (for GitHub Secrets)
cat ~/.ssh/github-deploy-key

# Display the public key (for VM)
cat ~/.ssh/github-deploy-key.pub
```

### Add Public Key to VMs

SSH into each VM and run:
```bash
# Add the public key to authorized_keys
echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
```

---

## Step 5: Configure GitHub Secrets

Go to your GitHub repository:
1. **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `STAGING_VM_HOST` | Staging VM IP (e.g., `20.10.30.40`) |
| `STAGING_VM_USER` | `azureuser` |
| `STAGING_VM_SSH_KEY` | Contents of `~/.ssh/github-deploy-key` |
| `PROD_VM_HOST` | Production VM IP |
| `PROD_VM_USER` | `azureuser` |
| `PROD_VM_SSH_KEY` | Contents of private key |

---

## Step 6: Configure GitHub Environments

For production deployment protection:

1. **Settings** → **Environments**
2. Click **New environment** → Name it `production`
3. Enable **Required reviewers**
4. Add yourself as a reviewer

This means production deployments will need approval!

---

## Step 7: Test SSH Connection

From your local machine:

```bash
# Test connection to staging
ssh -i ~/.ssh/github-deploy-key azureuser@<STAGING_VM_IP> "echo 'Connection successful!'"

# Test connection to production
ssh -i ~/.ssh/github-deploy-key azureuser@<PROD_VM_IP> "echo 'Connection successful!'"
```

---

## Architecture Diagram

```
Your Computer                    GitHub                         Azure
─────────────                    ──────                         ─────

   ┌──────┐     git push      ┌──────────┐                   ┌────────┐
   │ Code │ ─────────────────▶│Repository│                   │Staging │
   └──────┘                   └────┬─────┘                   │   VM   │
                                   │                         └────┬───┘
                                   │                              │
                              ┌────┴─────┐   SSH + rsync         │
                              │  GitHub  │ ──────────────────────┤
                              │ Actions  │                        │
                              └────┬─────┘                        │
                                   │                         ┌────┴───┐
                                   │   SSH + rsync           │  Prod  │
                                   └────────────────────────▶│   VM   │
                                                             └────────┘

Secrets stored in GitHub:
- STAGING_VM_HOST
- STAGING_VM_SSH_KEY
- PROD_VM_HOST
- PROD_VM_SSH_KEY
```

---

## Troubleshooting

### Can't SSH to VM
```bash
# Check if SSH port is open
nc -zv <VM_IP> 22

# Check Azure NSG rules allow port 22
az network nsg rule list -g flask-cicd-rg --nsg-name <NSG_NAME>
```

### Permission Denied
```bash
# Make sure private key has correct permissions
chmod 600 ~/.ssh/github-deploy-key

# Verify public key is in VM's authorized_keys
ssh azureuser@<VM_IP> "cat ~/.ssh/authorized_keys"
```

### Service Won't Start
```bash
# Check service status
sudo systemctl status flask-app

# Check logs
sudo journalctl -u flask-app -n 50
```

---

## Quiz

1. Why do we use two VMs (staging and production)?
2. What port does our Flask app run on?
3. Where do we store the SSH private key?
4. What does `systemctl enable flask-app` do?
5. How do we protect production deployments in GitHub?

---

## Next Module

[Module 5: Deployment to Staging](./05-DEPLOY-STAGING.md)
