# Scripts Directory

This directory contains organized automation and setup scripts for the OG-RAG project.

## Directory Structure

### `/automation/`
Contains scripts for automating various project tasks:

**GitHub Issue Management:**
- `add-issue.sh` - Add new GitHub issues
- `create-issues.sh` - Bulk create GitHub issues
- `create-github-labels.sh` - Create GitHub labels
- `debug-create-issue.sh` - Debug issue creation
- `debug-github-issues.py` - Python script for debugging GitHub issues
- `push-crisp-dm-issues.sh` - Push CRISP-DM related issues

**CRISP-DM Automation:**
- `create-crisp-dm-*.sh` - Various CRISP-DM creation scripts
- `update-crisp-dm-*.sh` - CRISP-DM update scripts

**Week-specific Scripts:**
- `create-week1-*.sh` - Week 1 project automation

**Smart Commit System:**
- `ai-smart-commit.sh` - AI-powered commit message generation
- `smart-commit.sh` - Smart commit functionality

**Utilities:**
- `check-deadlines.sh` - Check project deadlines
- `sync-progress.sh` - Sync project progress
- `update-estimates.sh` - Update time estimates
- `generate-report.sh` - Generate project reports
- `compile_literature_review.sh` - Compile literature review
- `test-script.sh` - General testing script
- `parse-issues.py` - Parse and process issues
- `project-fields.js` - Project field configurations

### `/setup/`
Contains installation and configuration scripts:

- `install-and-setup.sh` - Main installation and setup script
- `setup-smart-commit.sh` - Setup smart commit functionality

## Usage

To run any script, use:
```bash
# From the project root
./scripts/automation/[script-name]
./scripts/setup/[script-name]

# Or make them executable first
chmod +x scripts/automation/[script-name]
chmod +x scripts/setup/[script-name]
```

## Note

These scripts were moved from the root directory to keep the project structure clean and organized. All functionality remains the same, only the paths have changed.
