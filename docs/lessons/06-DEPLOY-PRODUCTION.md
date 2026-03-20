# Module 6: Production Deployment

## Why Production is Different

Production deployments need extra safety measures:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    STAGING vs PRODUCTION                                 │
├─────────────────────────────────┬───────────────────────────────────────┤
│           STAGING               │            PRODUCTION                  │
├─────────────────────────────────┼───────────────────────────────────────┤
│ Automatic deployment            │ Manual trigger only                    │
│ Test with fake data             │ Real user data                         │
│ OK if it breaks                 │ Must not break                         │
│ Few users (QA team)             │ Many users (customers)                 │
│ Can experiment                  │ Must be stable                         │
│ Quick rollback acceptable       │ Zero-downtime preferred                │
└─────────────────────────────────┴───────────────────────────────────────┘
```

---

## Production Safety Features

### 1. Manual Trigger Only
```yaml
on:
  workflow_dispatch:
    inputs:
      confirm_deployment:
        description: 'Type "deploy" to confirm'
        required: true
```

### 2. Confirmation Required
```yaml
- name: Confirm deployment
  if: ${{ github.event.inputs.confirm_deployment != 'deploy' }}
  run: |
    echo "❌ Deployment not confirmed"
    exit 1
```

### 3. Environment Protection
```yaml
environment:
  name: production
```

With required reviewers enabled in GitHub settings.

### 4. Pre-deployment Tests
```yaml
pre-deploy-tests:
  name: Run Tests Before Deploy
  steps:
    - run: pytest tests/ -v
```

### 5. Timestamped Backups
```yaml
BACKUP_DIR="/opt/flask-app-backup-$(date +%Y%m%d_%H%M%S)"
```

---

## Production Deployment Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Manual  │───▶│ Confirm  │───▶│  Tests   │───▶│ Approval │───▶│  Deploy  │
│ Trigger  │    │  Input   │    │   Pass   │    │(Optional)│    │   Prod   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────┐
                                                               │  Health  │
                                                               │  Check   │
                                                               └──────────┘
                                                                      │
                                                    ┌─────────────────┴─────────────────┐
                                                    ▼                                   ▼
                                              ┌──────────┐                       ┌──────────┐
                                              │ ✓ Success│                       │ ✗ Failed │
                                              │  Release │                       │ Rollback │
                                              │   Tag    │                       │ to backup│
                                              └──────────┘                       └──────────┘
```

---

## Setting Up Environment Protection

### Step 1: Create Production Environment

1. Go to **Repository Settings**
2. Click **Environments**
3. Click **New environment**
4. Name: `production`
5. Click **Configure environment**

### Step 2: Add Protection Rules

Enable these options:
- ✅ **Required reviewers** - Add yourself or team leads
- ✅ **Wait timer** - Optional delay (e.g., 5 minutes)
- ✅ **Deployment branches** - Limit to `main` only

---

## The Production Workflow

Key differences from staging:

### 1. Confirmation Input
```yaml
on:
  workflow_dispatch:
    inputs:
      confirm_deployment:
        description: 'Type "deploy" to confirm production deployment'
        required: true
        type: string
      version_tag:
        description: 'Version tag (e.g., v1.0.0)'
        required: false
        default: 'latest'
```

### 2. Validation Job
```yaml
jobs:
  validate:
    name: Validate Deployment
    steps:
      - name: Confirm deployment intent
        if: ${{ github.event.inputs.confirm_deployment != 'deploy' }}
        run: |
          echo "❌ Must type 'deploy' to confirm"
          exit 1
```

### 3. Pre-deployment Tests
```yaml
  pre-deploy-tests:
    needs: validate
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/ -v
```

### 4. Environment Declaration
```yaml
  deploy-production:
    needs: pre-deploy-tests
    environment:
      name: production
      url: http://${{ secrets.PROD_VM_HOST }}:5000
```

### 5. Version Tagging
```yaml
- name: Create Release
  uses: actions/create-release@v1
  with:
    tag_name: ${{ github.event.inputs.version_tag }}
    release_name: Release ${{ github.event.inputs.version_tag }}
```

---

## Hands-On Exercise

### Exercise 1: Deploy to Production

1. Go to **Actions** → **Deploy to Production**
2. Click **Run workflow**
3. Type `deploy` in the confirmation field
4. Enter version `v1.0.0`
5. Click **Run workflow**
6. If you set up required reviewers, approve the deployment
7. Watch it complete

### Exercise 2: Failed Confirmation

1. Trigger production deployment
2. Type `yes` instead of `deploy`
3. See it fail validation

### Exercise 3: Create a Release

1. Deploy with version `v1.1.0`
2. Go to **Releases** in your repository
3. See the new release created

---

## Production Checklist

Before deploying to production:

- [ ] All tests passing on staging
- [ ] QA approved staging deployment
- [ ] No known critical bugs
- [ ] Rollback plan ready
- [ ] Team notified of deployment
- [ ] Monitoring dashboards ready

---

## Monitoring After Deployment

### Check Application Health
```bash
curl http://<PROD_IP>:5000/health
```

### Check Logs
```bash
ssh azureuser@<PROD_IP>
sudo journalctl -u flask-app -f
```

### Check System Resources
```bash
ssh azureuser@<PROD_IP>
htop  # or top
```

---

## Rollback Procedures

### Automatic Rollback (in workflow)
The workflow automatically rolls back if health check fails.

### Manual Rollback
```bash
ssh azureuser@<PROD_IP>

# List available backups
ls -la /opt/flask-app-backup-*

# Restore specific backup
BACKUP="/opt/flask-app-backup-20240315_143022"
sudo rm -rf /opt/flask-app
sudo cp -r $BACKUP /opt/flask-app
sudo systemctl restart flask-app
```

---

## Quiz

1. Why is production deployment manual-only?
2. What is an "environment" in GitHub Actions?
3. What does "required reviewers" do?
4. Why do we run tests before production deployment?
5. How do you manually rollback a deployment?

---

## Summary

You've learned the complete CI/CD pipeline:

```
Code Push → CI (Build/Test/Lint) → Auto-deploy to Staging → Manual deploy to Production
                                          ↓                         ↓
                                    Health Check               Health Check
                                          ↓                         ↓
                                    Rollback if fail          Rollback if fail
```

---

## Next Steps

1. Add more tests
2. Set up monitoring (Prometheus, Grafana)
3. Add notifications (Slack, email)
4. Implement blue-green deployments
5. Add database migrations to pipeline
