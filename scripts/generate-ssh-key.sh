#!/bin/bash
# =============================================================================
# Generate SSH Key for GitHub Actions Deployment
# =============================================================================
# This script generates an SSH key pair for CI/CD deployments.
# The private key goes to GitHub Secrets, the public key goes to the VM.
#
# Usage: bash generate-ssh-key.sh
# =============================================================================

KEY_NAME="github-actions-deploy"
KEY_PATH="$HOME/.ssh/$KEY_NAME"

echo "🔑 Generating SSH key pair for GitHub Actions..."

# Generate key pair
ssh-keygen -t ed25519 -C "github-actions-deploy" -f "$KEY_PATH" -N ""

echo ""
echo "✅ SSH key pair generated!"
echo ""
echo "========================================"
echo "📋 INSTRUCTIONS"
echo "========================================"
echo ""
echo "1. COPY THE PRIVATE KEY TO GITHUB SECRETS:"
echo "   Go to: GitHub Repo → Settings → Secrets and variables → Actions"
echo "   Create secret named: STAGING_VM_SSH_KEY (or PROD_VM_SSH_KEY)"
echo "   Value:"
echo "----------------------------------------"
cat "$KEY_PATH"
echo ""
echo "----------------------------------------"
echo ""
echo "2. ADD THE PUBLIC KEY TO YOUR AZURE VM:"
echo "   SSH into your VM and run:"
echo "   echo '$(cat "$KEY_PATH.pub")' >> ~/.ssh/authorized_keys"
echo ""
echo "   Or copy this public key:"
echo "----------------------------------------"
cat "$KEY_PATH.pub"
echo "----------------------------------------"
echo ""
echo "3. ADD OTHER GITHUB SECRETS:"
echo "   - STAGING_VM_HOST: <your-staging-vm-ip>"
echo "   - STAGING_VM_USER: azureuser"
echo "   - PROD_VM_HOST: <your-prod-vm-ip>"
echo "   - PROD_VM_USER: azureuser"
