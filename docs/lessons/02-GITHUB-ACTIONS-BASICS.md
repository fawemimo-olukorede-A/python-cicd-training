# Module 2: GitHub Actions Basics

## What is GitHub Actions?

GitHub Actions is GitHub's built-in CI/CD platform. It allows you to automate workflows directly in your repository.

```
GitHub Repository
       │
       ├── .github/
       │   └── workflows/
       │       ├── ci.yml        ← Workflow files
       │       ├── deploy.yml
       │       └── test.yml
       │
       ├── src/
       └── README.md
```

---

## Key Components

### 1. Workflow
A YAML file that defines your automation. Lives in `.github/workflows/`.

### 2. Event (Trigger)
What starts the workflow:
- `push` - Code pushed to repository
- `pull_request` - PR opened or updated
- `workflow_dispatch` - Manual trigger
- `schedule` - Cron schedule

### 3. Job
A set of steps that run on a runner (virtual machine).

### 4. Step
A single task within a job.

### 5. Action
A reusable piece of code (like a plugin).

### 6. Runner
The server that executes your workflow (`ubuntu-latest`, `windows-latest`).

---

## Basic Workflow Structure

```yaml
# Name of the workflow (shown in GitHub UI)
name: My First Workflow

# When to run this workflow
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# The jobs to run
jobs:
  # Job ID (can be anything)
  build:
    # What machine to run on
    runs-on: ubuntu-latest

    # The steps in this job
    steps:
      # Step 1: Get the code
      - name: Checkout code
        uses: actions/checkout@v4

      # Step 2: Run a command
      - name: Say hello
        run: echo "Hello, World!"
```

---

## Common Triggers

### Push to Branch
```yaml
on:
  push:
    branches: [main, develop]
```

### Pull Request
```yaml
on:
  pull_request:
    branches: [main]
```

### Manual Trigger
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
```

### Scheduled (Cron)
```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am
```

### After Another Workflow
```yaml
on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
```

---

## Working with Steps

### Run Shell Commands
```yaml
steps:
  - name: Run commands
    run: |
      echo "First command"
      echo "Second command"
      ls -la
```

### Use Pre-built Actions
```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Setup Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.11'
```

### Set Environment Variables
```yaml
steps:
  - name: Set env
    run: echo "MY_VAR=hello" >> $GITHUB_ENV

  - name: Use env
    run: echo $MY_VAR  # Outputs: hello
```

---

## Using Secrets

Secrets are encrypted values stored in GitHub. Never put passwords in your code!

### Setting Secrets
1. Go to Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value

### Using Secrets
```yaml
steps:
  - name: Deploy with SSH
    run: |
      echo "${{ secrets.SSH_KEY }}" > key.pem
      ssh -i key.pem user@${{ secrets.SERVER_IP }}
```

---

## Job Dependencies

Jobs run in parallel by default. Use `needs` to run sequentially:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building..."

  test:
    runs-on: ubuntu-latest
    needs: build  # Waits for build to finish
    steps:
      - run: echo "Testing..."

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]  # Waits for both
    steps:
      - run: echo "Deploying..."
```

---

## Conditional Execution

### Run on Success
```yaml
steps:
  - name: Only on success
    if: success()
    run: echo "Previous steps passed!"
```

### Run on Failure
```yaml
steps:
  - name: Only on failure
    if: failure()
    run: echo "Something failed!"
```

### Run on Specific Branch
```yaml
steps:
  - name: Only on main
    if: github.ref == 'refs/heads/main'
    run: echo "On main branch!"
```

---

## Hands-On Exercise

Create a workflow file `.github/workflows/hello.yml`:

```yaml
name: Hello World

on:
  push:
    branches: [main]
  workflow_dispatch:  # Allows manual trigger

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Greet
        run: |
          echo "Hello from GitHub Actions!"
          echo "Repository: ${{ github.repository }}"
          echo "Branch: ${{ github.ref }}"
          echo "Triggered by: ${{ github.actor }}"
```

### Test Your Workflow
1. Push the file to your repository
2. Go to Actions tab
3. Watch it run!

---

## Common Actions

| Action | Purpose |
|--------|---------|
| `actions/checkout@v4` | Clone your repository |
| `actions/setup-python@v5` | Install Python |
| `actions/setup-node@v4` | Install Node.js |
| `actions/cache@v4` | Cache dependencies |
| `actions/upload-artifact@v4` | Save files from workflow |

---

## Quiz

1. Where do workflow files live?
2. What does `runs-on: ubuntu-latest` mean?
3. How do you run a step only if previous steps failed?
4. What is the `uses` keyword for?
5. How do you create a dependency between jobs?

---

## Next Module

[Module 3: Writing Your First CI Pipeline](./03-FIRST-CI-PIPELINE.md)
