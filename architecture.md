                         DEVOPS PIPELINE STRATEGY

┌──────────────┐
│  DEVELOPER   │
│ Write Code   │
│ git commit   │
└──────┬───────┘
       │ git push / PR
       ▼
┌──────────────────────────┐
│   GITHUB REPOSITORY      │
│ Source Control (main)    │
└────────┬─────────────────┘
         │ Triggers Workflow
         ▼
┌──────────────────────────┐
│   CI PIPELINE (ACTIONS)  │
│ ─ Checkout Code          │
│ ─ Setup Python           │
│ ─ Install Dependencies   │
│ ─ Run Tests              │
│ ─ Validate Build         │
└────────┬─────────────────┘
         │ Auto on push
         ▼
┌──────────────────────────┐
│   STAGING DEPLOYMENT     │
│ ─ Package Application    │
│ ─ Transfer to VM         │
│ ─ Deploy App             │
│ ─ Restart Service        │
│ ─ Health Checks          │
└────────┬─────────────────┘
         │ Auto after CI
         ▼
┌──────────────────────────┐
│   APPROVAL GATE          │
│  (Production Env)        │
│ ─ Team Lead Approval     │
│ ─ Instructor Approval    │
│ ─ No Admin Bypass        │
└────────┬─────────────────┘
         │ Manual approval required
         ▼
┌──────────────────────────┐
│  PRODUCTION DEPLOYMENT   │
│ ─ Package Release        │
│ ─ Transfer to Prod VM    │
│ ─ Deploy Application     │
│ ─ Restart Service        │
│ ─ Final Health Check     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│   LIVE APPLICATION       │
│   Users Access System    │
└──────────────────────────┘


---------------------------------------------------------------------------


👨‍💻 Developer
     │
     │  git push / pull request
     ▼
📦 GitHub Repository
     │
     │  ⚡ Triggers GitHub Actions
     ▼
🔧 CI Pipeline (Automated)
     ├── 📥 Checkout Code
     ├── 🐍 Setup Python
     ├── 📦 Install Dependencies
     ├── 🧪 Run Tests
     └── ✅ Validate Build
     │
     │  🚀 Auto on push
     ▼
🧪 Staging Deployment
     ├── 📦 Package Application
     ├── 📡 Transfer to Staging VM
     ├── ⚙️ Deploy Application
     ├── 🔄 Restart Service
     └── 🩺 Health Checks
     │
     │  🚀 Auto after CI
     ▼
⛔ Approval Gate (Production Environment)
     ├── 👨‍💼 Team Lead Approval
     ├── 🧑‍🏫 Instructor Approval
     └── 🔒 Admin Bypass Disabled
     │
     │  ✋ Manual approval required
     ▼
🚀 Production Deployment
     ├── 📦 Package Release
     ├── 📡 Transfer to Production VM
     ├── ⚙️ Deploy Application
     ├── 🔄 Restart Service
     └── 🩺 Final Health Check
     │
     ▼
🌍 Live Production Application




                         DEVOPS PIPELINE STRATEGY

┌──────────────┐
│  DEVELOPER   │
│ Write Code   │
│ git commit   │
└──────┬───────┘
       │ git push / PR
       ▼
┌──────────────────────────┐
│   GITHUB REPOSITORY      │
│ Source Control (main)    │
└────────┬─────────────────┘
         │ Triggers Workflow
         ▼
┌──────────────────────────┐
│   CI PIPELINE (ACTIONS)  │
│ ─ Checkout Code          │
│ ─ Setup Python           │
│ ─ Install Dependencies   │
│ ─ Run Tests              │
│ ─ Validate Build         │
└────────┬─────────────────┘
         │ Auto on push
         ▼
┌──────────────────────────┐
│   STAGING DEPLOYMENT     │
│ ─ Package Application    │
│ ─ Transfer to VM         │
│ ─ Deploy App             │
│ ─ Restart Service        │
│ ─ Health Checks          │
└────────┬─────────────────┘
         │ Auto after CI
         ▼
┌──────────────────────────┐
│   APPROVAL GATE          │
│  (Production Env)        │
│ ─ Team Lead Approval     │
│ ─ Instructor Approval    │
│ ─ No Admin Bypass        │
└────────┬─────────────────┘
         │ Manual approval required
         ▼
┌──────────────────────────┐
│  PRODUCTION DEPLOYMENT   │
│ ─ Package Release        │
│ ─ Transfer to Prod VM    │
│ ─ Deploy Application     │
│ ─ Restart Service        │
│ ─ Final Health Check     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│   LIVE APPLICATION       │
│   Users Access System    │
└──────────────────────────┘