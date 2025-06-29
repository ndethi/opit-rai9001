# GitHub Issue Automation - Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the GitHub Issue Automation system.

## 🔧 Quick Diagnostics

### Run System Health Check
```bash
# Basic health check
./test-script.sh unit

# Full system check with integration tests
./test-script.sh --integration all

# Check specific component
./test-script.sh parsing
```

### Verify Prerequisites
```bash
# Check GitHub CLI installation and authentication
gh --version
gh auth status

# Check Python dependencies
python3 -c "import json, re, datetime; print('Python modules OK')"

# Verify file structure
ls -la .github/issues/
```

## 🚨 Common Issues and Solutions

### 1. GitHub CLI Authentication Issues

#### Problem: `gh auth status` fails
```
Error: authentication required
```

#### Solutions:
```bash
# Re-authenticate with GitHub
gh auth login

# Use token authentication
gh auth login --with-token < your-token.txt

# Check scopes (need repo, project access)
gh auth status --show-token
```

#### Problem: Permission denied for repository operations
```
Error: HTTP 403: Forbidden
```

#### Solutions:
- Verify you have write access to the repository
- Check if organization requires SSO authentication:
```bash
gh auth refresh -s admin:org
```
- Ensure your token has required scopes: `repo`, `write:org`, `project`

### 2. Issue Creation Failures

#### Problem: Issues not created despite successful parsing
```bash
# Debug with verbose mode
./create-issues.sh --verbose --dry-run

# Check rate limiting
./create-issues.sh --rate-limit 2
```

#### Problem: Invalid issue format or missing fields
```bash
# Validate markdown format
./parse-issues.py --file .github/issues/consolidated-issues.md --validate

# Check specific issue
./add-issue.sh extract ISSUE_ID
```

#### Common Format Issues:
1. **Missing required fields**: Ensure `**TITLE:**`, `**LABELS:**` are present
2. **Invalid date format**: Use `YYYY-MM-DD` for due dates
3. **Malformed JSON in project fields**: Validate JSON syntax
4. **Special characters in titles**: Escape or remove problematic characters

### 3. Parsing Errors

#### Problem: Python script fails with import errors
```bash
# Install missing dependencies
pip3 install json re datetime argparse

# Check Python version (requires 3.6+)
python3 --version
```

#### Problem: Markdown parsing returns empty results
```
Parsed 0 issues from consolidated-issues.md
```

#### Debugging Steps:
```bash
# Check file content and encoding
file .github/issues/consolidated-issues.md
head -20 .github/issues/consolidated-issues.md

# Test with verbose parsing
python3 parse-issues.py --file .github/issues/consolidated-issues.md --verbose

# Validate markdown structure
grep -n "^##" .github/issues/consolidated-issues.md
```

#### Common Parsing Issues:
1. **Incorrect section headers**: Must start with `## ISSUE_ID` or `## WEEK_X_SPRINT`
2. **Missing field markers**: Fields must use `**FIELD:**` format exactly
3. **Encoding issues**: Ensure UTF-8 encoding
4. **Line ending problems**: Convert to Unix line endings if needed

### 4. Project Fields Integration

#### Problem: Project fields not updating
```bash
# Check Node.js and npm availability
node --version
npm --version

# Install dependencies
npm install @octokit/graphql

# Test GraphQL connection
node project-fields.js --test-connection
```

#### Problem: Field mapping errors
```
Error: Field "Priority" not found in project
```

#### Solutions:
1. **Verify project configuration**:
```bash
# List available projects
gh project list

# Check project fields
gh project field-list --owner OWNER --number PROJECT_NUMBER
```

2. **Update field mappings** in `project-fields.js`:
```javascript
const FIELD_MAPPINGS = {
    'Priority': 'Priority',  // Ensure exact field name match
    'Status': 'Status',
    'Iteration': 'Sprint'
};
```

### 5. Synchronization Issues

#### Problem: Local and GitHub issues out of sync
```bash
# Force sync with conflict resolution
./sync-progress.sh --direction local-to-github --verbose

# Preview sync changes
./sync-progress.sh --dry-run
```

#### Problem: Duplicate issues created
```bash
# Check for existing issues before creating
gh issue list --label "duplicate-check"

# Use issue ID matching to prevent duplicates
./create-issues.sh --skip-existing
```

### 6. Performance and Rate Limiting

#### Problem: API rate limit exceeded
```
Error: API rate limit exceeded
```

#### Solutions:
```bash
# Increase delay between requests
./create-issues.sh --rate-limit 5

# Use smaller batch sizes
./create-issues.sh --batch-size 5

# Check current rate limit status
gh api rate_limit
```

#### Optimization Tips:
- Run during off-peak hours
- Use authenticated requests (higher rate limits)
- Implement exponential backoff for retries
- Cache results when possible

### 7. File Permission and Access Issues

#### Problem: Permission denied writing to files
```bash
# Check file permissions
ls -la .github/issues/

# Fix permissions
chmod 644 .github/issues/*.md
chmod 755 *.sh

# Check directory ownership
stat .github/issues/
```

#### Problem: Backup creation fails
```bash
# Check backup directory permissions
mkdir -p .github/issues/backups
chmod 755 .github/issues/backups

# Verify disk space
df -h .
```

### 8. Network and Connectivity Issues

#### Problem: GitHub API timeouts
```
Error: request timeout
```

#### Solutions:
```bash
# Test connectivity
ping api.github.com

# Use alternative endpoints if available
export GITHUB_API_URL="https://api.github.com"

# Increase timeout values
./create-issues.sh --timeout 30
```

#### Problem: SSL/TLS certificate errors
```bash
# Update certificates
brew update && brew upgrade ca-certificates  # macOS
sudo apt-get update && sudo apt-get install ca-certificates  # Ubuntu

# Test SSL connection
openssl s_client -connect api.github.com:443
```

## 🔍 Debugging Tools and Techniques

### Enable Debug Mode
```bash
# Set debug environment variables
export DEBUG=1
export VERBOSE=true

# Run with maximum verbosity
./create-issues.sh --verbose --dry-run 2>&1 | tee debug.log
```

### Inspect Intermediate Files
```bash
# Check parsed JSON output
python3 parse-issues.py --file .github/issues/consolidated-issues.md --output debug-issues.json
jq . debug-issues.json

# Verify issue creation payload
./create-issues.sh --dry-run --verbose | grep -A 10 "Issue payload"
```

### Log Analysis
```bash
# Check automation logs
tail -f issue-automation.log

# Search for specific errors
grep -i "error\|fail" *.log

# Analyze timestamps and patterns
awk '/ERROR/ {print $1, $2, $NF}' issue-automation.log
```

### Network Debugging
```bash
# Monitor API calls
export GH_DEBUG=api
gh issue list --limit 1

# Capture network traffic (if needed)
tcpdump -i en0 host api.github.com
```

## 📊 Performance Monitoring

### Monitor Resource Usage
```bash
# Check memory usage during operation
./create-issues.sh &
PID=$!
while kill -0 $PID 2>/dev/null; do
    ps -o pid,rss,vsz,comm $PID
    sleep 5
done
```

### Benchmark Operations
```bash
# Time issue creation
time ./create-issues.sh --dry-run

# Profile parsing performance
time python3 parse-issues.py --file .github/issues/consolidated-issues.md --output /dev/null
```

## 🔄 Recovery Procedures

### Restore from Backup
```bash
# List available backups
ls -la .github/issues/backups/

# Restore specific backup
cp .github/issues/backups/consolidated-issues_20250120_143022.md .github/issues/consolidated-issues.md

# Verify restoration
./parse-issues.py --file .github/issues/consolidated-issues.md --output /tmp/test.json
```

### Clean Up Failed Operations
```bash
# Remove partial issue creations (dry run first)
gh issue list --label "automation-temp" --json number --jq '.[].number' | while read num; do
    echo "Would delete issue #$num"
    # gh issue delete $num --confirm  # Uncomment to actually delete
done

# Clean up temporary files
rm -f /tmp/*issues*.json
rm -f .tmp/*
```

### Reset Configuration
```bash
# Backup current config
cp .github-automation-config .github-automation-config.backup

# Reset to defaults
rm .github-automation-config
./install-and-setup.sh --reconfigure
```

## 🧪 Test Scenarios

### Validate Full Workflow
```bash
# 1. Create test issue
./add-issue.sh create --test-mode

# 2. Parse and validate
./parse-issues.py --file .github/issues/consolidated-issues.md --validate

# 3. Test creation (dry run)
./create-issues.sh --dry-run

# 4. Test utilities
./generate-report.sh --type summary
./check-deadlines.sh --format summary
```

### Stress Testing
```bash
# Test with large number of issues
./test-script.sh --verbose unit

# Simulate high load
for i in {1..10}; do
    ./create-issues.sh --dry-run &
done
wait
```

## 📞 Getting Help

### Community Resources
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Project Issues](https://github.com/your-repo/issues)

### Self-Help Tools
```bash
# Built-in help
./create-issues.sh --help
./parse-issues.py --help
./sync-progress.sh --help

# System diagnostics
./test-script.sh --verbose all > diagnostic-report.txt 2>&1
```

### Collecting Debug Information
When reporting issues, include:

1. **System Information**:
```bash
uname -a
python3 --version
gh --version
node --version 2>/dev/null || echo "Node.js not installed"
```

2. **Error Logs**:
```bash
# Last 50 lines of logs
tail -50 issue-automation.log

# Specific error context
grep -B 5 -A 5 "ERROR" *.log
```

3. **Configuration**:
```bash
# Sanitized config (remove tokens)
cat .github-automation-config | sed 's/token=.*/token=***REDACTED***/'
```

4. **Test Results**:
```bash
# Recent test output
./test-script.sh unit > test-results.txt 2>&1
```

## 🛡️ Security Considerations

### Token Security
- Never commit tokens to version control
- Use environment variables or secure files for tokens
- Regularly rotate access tokens
- Use minimum required scopes

### File Permissions
```bash
# Secure sensitive files
chmod 600 .github-automation-config
chmod 600 ~/.config/gh/hosts.yml
```

### Audit Trail
```bash
# Review automation actions
gh issue list --author "@me" --label "automation"

# Check project field updates
gh api graphql -f query='{ viewer { login } }'
```

---

*Last updated: $(date '+%Y-%m-%d')*
*For additional support, create an issue with the "help" label.*
