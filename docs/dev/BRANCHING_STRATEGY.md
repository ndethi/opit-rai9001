# thiLLMo Git Branching Strategy

## Branch Structure

### 🌿 **Main Branches**

- **`main`** - Production-ready code
  - Only merge from `dev` after thorough testing
  - Protected branch for stable releases
  - Tagged with version numbers (v0.1.0, v0.2.0, etc.)

- **`dev`** - Primary development branch
  - All feature development happens here
  - Integration branch for testing before main
  - Where daily work and commits occur

### 🔀 **Supporting Branches**

- **`feature/*`** - New features
  - Branch from: `dev`
  - Merge back to: `dev`
  - Example: `feature/ontology-schema`, `feature/rag-pipeline`

- **`fix/*`** - Bug fixes
  - Branch from: `dev` (or `main` for hotfixes)
  - Merge back to: `dev` (and `main` for hotfixes)
  - Example: `fix/pronunciation-guide`, `fix/prompt-logging`

- **`docs/*`** - Documentation updates
  - Branch from: `dev`
  - Merge back to: `dev`
  - Example: `docs/readme-update`, `docs/api-documentation`

## Workflow Process

### 🚀 **Daily Development**
```bash
# Work on dev branch
git checkout dev
git pull origin dev

# Make changes and commit
git add .
cz commit

# Push to dev
git push origin dev
```

### 🎯 **Feature Development**
```bash
# Create feature branch
git checkout dev
git pull origin dev
git checkout -b feature/new-feature

# Work and commit
git add .
cz commit

# Push feature branch
git push origin feature/new-feature

# Merge back to dev when complete
git checkout dev
git merge feature/new-feature
git push origin dev
```

### 🎉 **Release to Main**
```bash
# When dev is stable and tested
git checkout main
git pull origin main
git merge dev
git push origin main

# Tag the release
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## Branch Protection Rules

- **Main branch**: Requires pull request reviews
- **Dev branch**: Direct commits allowed for primary development
- **Feature branches**: Temporary, delete after merge

## Current Status

- ✅ **Main branch**: Stable foundation with project setup
- 🔄 **Dev branch**: Active development branch (current)
- 📋 **Next**: Feature branches as needed for specific components
