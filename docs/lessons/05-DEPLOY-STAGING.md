# Module 5: Deployment to Staging

## Objective

Create a CD pipeline that automatically deploys to staging after CI passes.

---

## Staging Deployment Flow

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  CI Passes │────▶│  Package   │────▶│  Copy to   │────▶│   Deploy   │
│            │     │    App     │     │     VM     │     │ & Restart  │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
                                                                │
                                                                ▼
                                                         ┌────────────┐
                                                         │   Health   │
                                                         │   Check    │
                                                         └────────────┘
                                                                │
                                            ┌───────────────────┴───────────────────┐
                                            ▼                                       ▼
                                      ┌──────────┐                           ┌──────────┐
                                      │  ✓ Pass  │                           │  ✗ Fail  │
                                      │  Done!   │                           │ Rollback │
                                      └──────────┘                           └──────────┘
```

---

## The Deployment Workflow

Create `.github/workflows/deploy-staging.yml`:

### Part 1: Trigger and Setup

```yaml
name: Deploy to Staging

on:
  # Trigger after CI workflow completes
  workflow_run:
    workflows: ["CI Pipeline"]
    branches: [main]
    types:
      - completed

  # Allow manual trigger
  workflow_dispatch:

jobs:
  deploy-staging:
    name: Deploy to Staging VM
    runs-on: ubuntu-latest

    # Only run if CI passed
    if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'workflow_dispatch' }}
```

**Key Concepts:**
- `workflow_run`: Triggers after another workflow finishes
- `workflow_dispatch`: Allows manual trigger from GitHub UI
- `if`: Conditional - only runs if CI passed

---

### Part 2: Set Up SSH

```yaml
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up SSH key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.STAGING_VM_SSH_KEY }}" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key
          ssh-keyscan -H ${{ secrets.STAGING_VM_HOST }} >> ~/.ssh/known_hosts
```

**What's happening:**
1. Create SSH directory
2. Write private key from GitHub Secrets
3. Set correct permissions (600 = owner read/write only)
4. Add VM to known hosts (prevents "unknown host" prompt)

---

### Part 3: Create Deployment Package

```yaml
      - name: Create deployment package
        run: |
          mkdir -p deploy_package
          cp -r app.py templates static requirements.txt deploy_package/
          tar -czf deploy.tar.gz deploy_package
```

**Why package?**
- Only include necessary files
- Faster transfer (compressed)
- Clean deployment every time

---

### Part 4: Copy Files to VM

```yaml
      - name: Copy files to Staging VM
        run: |
          scp -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no \
            deploy.tar.gz \
            ${{ secrets.STAGING_VM_USER }}@${{ secrets.STAGING_VM_HOST }}:/tmp/
```

**Commands explained:**
- `scp`: Secure copy over SSH
- `-i ~/.ssh/deploy_key`: Use our SSH key
- `-o StrictHostKeyChecking=no`: Don't prompt for unknown host
- Copies `deploy.tar.gz` to `/tmp/` on the VM

---

### Part 5: Deploy on the VM

```yaml
      - name: Deploy application
        run: |
          ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no \
            ${{ secrets.STAGING_VM_USER }}@${{ secrets.STAGING_VM_HOST }} << 'DEPLOY'

            set -e  # Exit on error

            echo "🚀 Starting deployment..."

            # Define paths
            APP_DIR="/opt/flask-app"
            BACKUP_DIR="/opt/flask-app-backup"

            # Backup current version
            if [ -d "$APP_DIR" ]; then
              sudo rm -rf $BACKUP_DIR
              sudo cp -r $APP_DIR $BACKUP_DIR
            fi

            # Extract new version
            cd /tmp
            tar -xzf deploy.tar.gz
            sudo mkdir -p $APP_DIR
            sudo cp -r deploy_package/* $APP_DIR/

            # Setup Python environment
            cd $APP_DIR
            sudo python3 -m venv venv
            sudo $APP_DIR/venv/bin/pip install -r requirements.txt

            # Restart application
            sudo systemctl restart flask-app

            echo "✅ Deployment complete!"

          DEPLOY
```

**Deployment steps:**
1. `set -e`: Stop on any error
2. Create backup of current version
3. Extract new files
4. Install Python dependencies
5. Restart the service

---

### Part 6: Health Check

```yaml
      - name: Health Check
        run: |
          sleep 5  # Wait for app to start

          HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
            http://${{ secrets.STAGING_VM_HOST }}:5000/health)

          if [ "$HTTP_STATUS" -eq 200 ]; then
            echo "✅ Health check passed!"
          else
            echo "❌ Health check failed with status: $HTTP_STATUS"
            exit 1
          fi
```

**Why health check?**
- Verify app is actually running
- Catch deployment failures early
- Trigger rollback if needed

---

### Part 7: Rollback on Failure (Advanced)

Add this to the deployment script:

```bash
# After health check fails
if [ "$HTTP_STATUS" -ne 200 ]; then
  echo "🔙 Rolling back..."
  sudo rm -rf $APP_DIR
  sudo mv $BACKUP_DIR $APP_DIR
  sudo systemctl restart flask-app
  exit 1
fi
```

---

## Complete Staging Workflow

See `.github/workflows/02-cd-staging.yml` in the repository.

---

## Hands-On Exercise

### Exercise 1: Manual Deploy

1. Go to **Actions** tab
2. Select **Deploy to Staging**
3. Click **Run workflow**
4. Watch the deployment
5. Visit `http://<STAGING_IP>:5000/health`

### Exercise 2: Automatic Deploy

1. Make a small change to `app.py`
2. Push to `main` branch
3. Watch CI run, then staging deploy

### Exercise 3: Trigger a Rollback

1. Add code that breaks the app:
   ```python
   @app.route('/health')
   def health_check():
       raise Exception("Intentional error")
   ```
2. Push and watch the deployment fail
3. Verify rollback happened

---

## Debugging Deployments

### Check VM logs
```bash
ssh azureuser@<STAGING_IP>
sudo journalctl -u flask-app -n 100
```

### Check if app is running
```bash
ssh azureuser@<STAGING_IP>
sudo systemctl status flask-app
```

### Test locally on VM
```bash
ssh azureuser@<STAGING_IP>
curl http://localhost:5000/health
```

---

## Quiz

1. What triggers the staging deployment?
2. Why do we create a backup before deploying?
3. What does `set -e` do in a bash script?
4. How do we check if deployment succeeded?
5. What happens if the health check fails?

---

## Next Module

[Module 6: Production Deployment](./06-DEPLOY-PRODUCTION.md)
