# Module 1: CI/CD Fundamentals

## What is CI/CD?

**CI/CD** stands for **Continuous Integration** and **Continuous Deployment/Delivery**.

### Continuous Integration (CI)

CI is the practice of automatically building and testing code every time a developer pushes changes.

```
Without CI:                          With CI:
─────────────                        ────────
Developer A pushes code              Developer A pushes code
Developer B pushes code              → Automatic build
Nobody tests                         → Automatic tests
Bugs accumulate                      → Instant feedback
Friday: "Why is everything broken?"  → Bugs caught immediately
```

**Key CI Activities:**
- ✅ Build the application
- ✅ Run unit tests
- ✅ Run integration tests
- ✅ Code linting (style checks)
- ✅ Security scanning

### Continuous Deployment (CD)

CD automatically deploys code to servers after CI passes.

```
Code Push → CI (Build/Test) → CD (Deploy to Staging) → CD (Deploy to Production)
```

**Key CD Activities:**
- ✅ Package the application
- ✅ Deploy to staging environment
- ✅ Run smoke tests
- ✅ Deploy to production
- ✅ Monitor for issues

---

## Why CI/CD Matters

### Without CI/CD (Manual Process)

```
1. Developer finishes feature
2. Developer manually runs tests (maybe)
3. Developer asks ops team to deploy
4. Ops team manually copies files to server
5. Something breaks
6. Everyone panics
7. Rollback takes hours
```

### With CI/CD (Automated Process)

```
1. Developer pushes code
2. Pipeline automatically runs tests
3. Tests pass → automatic deploy to staging
4. QA tests on staging
5. One-click deploy to production
6. Something breaks → automatic rollback
7. Issue fixed in minutes
```

---

## CI/CD Pipeline Stages

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  CODE   │───▶│  BUILD  │───▶│  TEST   │───▶│ STAGING │───▶│  PROD   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │              │
  Commit       Install deps    Unit tests    Deploy to      Deploy to
  changes      Compile         Integration   test server    live server
               Package         Lint
```

### Stage 1: Code
- Developer writes code
- Commits to Git
- Pushes to GitHub

### Stage 2: Build
- Install dependencies (`pip install`)
- Compile if needed
- Create deployment package

### Stage 3: Test
- **Unit tests**: Test individual functions
- **Integration tests**: Test components together
- **Linting**: Check code style
- **Security scan**: Check for vulnerabilities

### Stage 4: Staging (Test Environment)
- Deploy to a test server
- Run smoke tests
- QA team can test
- Mirrors production setup

### Stage 5: Production
- Deploy to live server
- Users can access
- Monitor for issues
- Automatic rollback if needed

---

## Key Concepts

### 1. Pipeline
A series of automated steps that code goes through.

### 2. Job
A set of steps that run on the same machine.

### 3. Step
A single task (e.g., "run tests", "deploy to server").

### 4. Trigger
What starts the pipeline (e.g., push, pull request).

### 5. Artifact
Files produced by the pipeline (e.g., test reports, packages).

### 6. Environment
Where code runs (staging, production).

### 7. Secret
Sensitive data stored securely (passwords, SSH keys).

---

## Exercise: Draw Your Own Pipeline

On paper, draw a CI/CD pipeline for a web application with these requirements:
- Run tests on every push
- Deploy to staging on merge to main
- Require manual approval for production

---

## Quiz

1. What does CI stand for?
2. What happens in the "Build" stage?
3. Why do we deploy to staging before production?
4. What is a "secret" in CI/CD?
5. Name two benefits of CI/CD.

---

## Next Module

[Module 2: GitHub Actions Basics](./02-GITHUB-ACTIONS-BASICS.md)
