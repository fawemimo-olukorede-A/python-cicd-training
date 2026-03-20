# CI/CD Pipeline Training - Complete Guide

## Training Overview

This training will take students from zero to deploying applications using CI/CD pipelines with GitHub Actions and Azure VMs.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CI/CD PIPELINE ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

    Developer                 GitHub                    Azure VMs
    ─────────                 ──────                    ─────────
        │                        │                          │
        │  git push              │                          │
        ├───────────────────────►│                          │
        │                        │                          │
        │                   ┌────┴────┐                     │
        │                   │   CI    │                     │
        │                   │ Pipeline│                     │
        │                   │         │                     │
        │                   │ • Build │                     │
        │                   │ • Test  │                     │
        │                   │ • Lint  │                     │
        │                   └────┬────┘                     │
        │                        │                          │
        │                        │ If tests pass            │
        │                        ▼                          │
        │                   ┌─────────┐     SSH + rsync     │
        │                   │   CD    │────────────────────►│ STAGING VM
        │                   │ Staging │                     │ (test environment)
        │                   └────┬────┘                     │
        │                        │                          │
        │                        │ Manual approval          │
        │                        ▼                          │
        │                   ┌─────────┐     SSH + rsync     │
        │                   │   CD    │────────────────────►│ PRODUCTION VM
        │                   │  Prod   │                     │ (live environment)
        │                   └─────────┘                     │
        │                        │                          │
        │◄───────────────────────┤                          │
        │  Notification          │                          │
```

## Training Modules

| Module | Topic | Duration | Level |
|--------|-------|----------|-------|
| 1 | CI/CD Fundamentals | 30 min | Beginner |
| 2 | GitHub Actions Basics | 45 min | Beginner |
| 3 | Writing Your First Pipeline | 60 min | Beginner |
| 4 | Testing in CI/CD | 45 min | Intermediate |
| 5 | Azure VM Setup | 30 min | Intermediate |
| 6 | Deployment to Staging | 60 min | Intermediate |
| 7 | Production Deployment | 45 min | Advanced |
| 8 | Advanced Topics | 60 min | Advanced |

## Prerequisites

- GitHub account
- Azure account with VM access
- Basic Python knowledge
- Basic Git knowledge

## Project Structure

```
python-cicd-training/
├── .github/
│   └── workflows/
│       ├── 01-ci.yml              # Lesson: CI Pipeline
│       ├── 02-cd-staging.yml      # Lesson: Deploy to Staging
│       └── 03-cd-production.yml   # Lesson: Deploy to Production
├── app.py                         # Flask application
├── templates/                     # HTML templates
├── static/                        # Static files
├── tests/
│   └── test_app.py               # Unit & integration tests
├── scripts/
│   ├── vm-setup.sh               # Azure VM setup script
│   └── generate-ssh-key.sh       # SSH key generator
├── requirements.txt              # Python dependencies
└── docs/
    └── lessons/                  # Training materials
```

## Quick Start (For Trainers)

1. **Fork this repository** to your GitHub account
2. **Provision two Azure VMs** (staging + production)
3. **Run VM setup script** on both VMs
4. **Configure GitHub Secrets** (SSH keys, VM IPs)
5. **Follow the lesson modules** in order

## GitHub Secrets Required

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `STAGING_VM_HOST` | Staging VM IP address | `20.10.30.40` |
| `STAGING_VM_USER` | SSH username | `azureuser` |
| `STAGING_VM_SSH_KEY` | Private SSH key | `-----BEGIN OPENSSH...` |
| `PROD_VM_HOST` | Production VM IP address | `20.10.30.50` |
| `PROD_VM_USER` | SSH username | `azureuser` |
| `PROD_VM_SSH_KEY` | Private SSH key | `-----BEGIN OPENSSH...` |
