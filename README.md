# CI/CD Pipeline Training with GitHub Actions & Azure VMs

A complete, hands-on training course for learning CI/CD pipelines from beginner to advanced.

## Pipeline Overview

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  PUSH   │────▶│  BUILD  │────▶│  TEST   │────▶│ STAGING │────▶│  PROD   │
│  CODE   │     │ INSTALL │     │  LINT   │     │   VM    │     │   VM    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
                                     │               │               │
                               Auto on push    Auto after CI   Manual trigger
                                                                + approval
```

## Quick Start

### 1. Fork this repository

### 2. Set up Azure VMs
```bash
# SSH into your VM and run:
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/python-cicd-training/main/scripts/vm-setup.sh | sudo bash
```

### 3. Configure GitHub Secrets

| Secret | Description |
|--------|-------------|
| `STAGING_VM_HOST` | Staging VM IP address |
| `STAGING_VM_USER` | SSH username (azureuser) |
| `STAGING_VM_SSH_KEY` | SSH private key |
| `PROD_VM_HOST` | Production VM IP address |
| `PROD_VM_USER` | SSH username (azureuser) |
| `PROD_VM_SSH_KEY` | SSH private key |

### 4. Push code and watch the magic!

## Training Modules

| # | Module | File | Level |
|---|--------|------|-------|
| 0 | Training Overview | [00-TRAINING-OVERVIEW.md](docs/lessons/00-TRAINING-OVERVIEW.md) | - |
| 1 | CI/CD Fundamentals | [01-CICD-FUNDAMENTALS.md](docs/lessons/01-CICD-FUNDAMENTALS.md) | Beginner |
| 2 | GitHub Actions Basics | [02-GITHUB-ACTIONS-BASICS.md](docs/lessons/02-GITHUB-ACTIONS-BASICS.md) | Beginner |
| 3 | First CI Pipeline | [03-FIRST-CI-PIPELINE.md](docs/lessons/03-FIRST-CI-PIPELINE.md) | Beginner |
| 4 | Azure VM Setup | [04-AZURE-VM-SETUP.md](docs/lessons/04-AZURE-VM-SETUP.md) | Intermediate |
| 5 | Deploy to Staging | [05-DEPLOY-STAGING.md](docs/lessons/05-DEPLOY-STAGING.md) | Intermediate |
| 6 | Deploy to Production | [06-DEPLOY-PRODUCTION.md](docs/lessons/06-DEPLOY-PRODUCTION.md) | Advanced |

## Workflows

### CI Pipeline (`01-ci.yml`)
- Runs on every push/PR
- Installs dependencies
- Runs linting (flake8)
- Runs tests (pytest)

### Deploy to Staging (`02-cd-staging.yml`)
- Triggers after CI passes
- Deploys to staging VM via SSH
- Runs health checks
- Auto-rollback on failure

### Deploy to Production (`03-cd-production.yml`)
- Manual trigger only
- Requires confirmation ("deploy")
- Environment protection with approvers
- Creates release tags

## Project Structure

```
.
├── .github/workflows/
│   ├── 01-ci.yml              # CI Pipeline
│   ├── 02-cd-staging.yml      # Staging Deployment
│   └── 03-cd-production.yml   # Production Deployment
├── app.py                     # Flask application
├── templates/                 # HTML templates
├── static/                    # Static assets
├── tests/
│   └── test_app.py           # Unit tests
├── scripts/
│   ├── vm-setup.sh           # VM setup script
│   └── generate-ssh-key.sh   # SSH key generator
├── docs/lessons/             # Training materials
└── requirements.txt          # Python dependencies
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/health` | GET | Health check (for CI/CD) |
| `/ready` | GET | Readiness check |
| `/hello` | POST | Greeting form |
| `/api/greet/<name>` | GET | JSON greeting |
| `/api/add` | POST | Calculator (for testing) |

## Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/python-cicd-training.git
cd python-cicd-training

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Run tests
pytest tests/ -v
```

## Architecture

```
                    GitHub Actions
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 │                 ▼
  ┌───────────┐           │          ┌───────────┐
  │ STAGING   │           │          │PRODUCTION │
  │ Azure VM  │           │          │ Azure VM  │
  │           │           │          │           │
  │ Port 5000 │           │          │ Port 5000 │
  └───────────┘           │          └───────────┘
                          │
                   SSH + rsync
```

## Original Sample

This project is based on [Azure Samples Flask Quickstart](https://github.com/Azure-Samples/msdocs-python-flask-webapp-quickstart), enhanced with CI/CD training materials for Azure VM deployment.

## License

MIT License - Use freely for educational purposes.
