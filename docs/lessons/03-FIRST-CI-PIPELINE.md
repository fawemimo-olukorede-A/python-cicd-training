# Module 3: Writing Your First CI Pipeline

## Objective

Build a complete CI pipeline that:
1. Checks out code
2. Sets up Python
3. Installs dependencies
4. Runs linting
5. Runs tests

---

## The Pipeline We'll Build

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Push   │───▶│Checkout │───▶│  Setup  │───▶│  Lint   │───▶│  Test   │
│  Code   │    │  Code   │    │ Python  │    │ (flake8)│    │(pytest) │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## Step-by-Step Guide

### Step 1: Create the Workflow File

Create `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

**Explanation:**
- `name`: Displayed in GitHub Actions UI
- `on.push`: Runs when code is pushed to main or develop
- `on.pull_request`: Runs when a PR targets main

---

### Step 2: Define the Job

```yaml
jobs:
  build-and-test:
    name: Build & Test
    runs-on: ubuntu-latest
```

**Explanation:**
- `build-and-test`: Job ID (internal reference)
- `name`: Display name in UI
- `runs-on`: The virtual machine type

---

### Step 3: Checkout Code

```yaml
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
```

**Why?** The runner starts empty. We need to clone our repository.

---

### Step 4: Setup Python

```yaml
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
```

**Why?** We need Python installed to run our Flask app.

---

### Step 5: Cache Dependencies (Optional but Recommended)

```yaml
      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
```

**Why?** Downloading packages every time is slow. Caching speeds up builds.

---

### Step 6: Install Dependencies

```yaml
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
```

**Why?** We need Flask, pytest, and other packages.

---

### Step 7: Run Linting

```yaml
      - name: Run Flake8 Linting
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

**Why?** Linting catches syntax errors and style issues.

**Flake8 Error Codes:**
- `E9`: Syntax errors
- `F63`: Invalid escape sequences
- `F7`: Syntax errors in type comments
- `F82`: Undefined names

---

### Step 8: Run Tests

```yaml
      - name: Run Tests
        run: |
          pytest tests/ -v --cov=. --cov-report=term-missing
```

**Why?** Tests verify our code works correctly.

**Flags Explained:**
- `-v`: Verbose output
- `--cov=.`: Generate coverage report
- `--cov-report=term-missing`: Show which lines aren't tested

---

## Complete CI Pipeline

Here's the full `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    name: Build & Test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Flake8 Linting
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

      - name: Run Tests
        run: |
          pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## Hands-On Exercise

### Exercise 1: Make the Pipeline Fail

1. Edit `app.py` and introduce a syntax error:
   ```python
   def broken_function(
       return "This won't work"
   ```

2. Commit and push
3. Watch the pipeline fail
4. Fix the error and push again

### Exercise 2: Make a Test Fail

1. Edit `tests/test_app.py`:
   ```python
   def test_intentional_failure(self, client):
       assert 1 == 2  # This will fail!
   ```

2. Commit and push
3. See the test failure in the Actions tab
4. Remove the failing test

### Exercise 3: Add a New Test

1. Add a test for the `/api/greet/` endpoint
2. Push and verify it passes

---

## Understanding the Output

When you go to the Actions tab, you'll see:

```
CI Pipeline
├── build-and-test
│   ├── ✓ Set up job (2s)
│   ├── ✓ Checkout code (1s)
│   ├── ✓ Set up Python (5s)
│   ├── ✓ Cache pip dependencies (1s)
│   ├── ✓ Install dependencies (15s)
│   ├── ✓ Run Flake8 Linting (3s)
│   ├── ✓ Run Tests (5s)
│   └── ✓ Complete job (0s)
```

Click on any step to see its output.

---

## Common Issues and Solutions

### Issue: Tests not found
**Error:** `collected 0 items`
**Solution:** Make sure test files start with `test_` and test functions start with `test_`

### Issue: Module not found
**Error:** `ModuleNotFoundError: No module named 'flask'`
**Solution:** Check `requirements.txt` has all dependencies

### Issue: Linting failures blocking deployment
**Solution:** Use `--exit-zero` to warn without failing, or fix all lint errors

---

## Quiz

1. What does `actions/checkout@v4` do?
2. Why do we cache pip dependencies?
3. What command runs the tests?
4. How can you see why a pipeline failed?
5. What does `--cov=.` mean in pytest?

---

## Next Module

[Module 4: Writing Effective Tests](./04-TESTING.md)
