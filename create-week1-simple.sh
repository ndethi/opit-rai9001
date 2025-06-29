#!/bin/bash

# Simple Week 1 issue creator
set -e

# Disable GitHub CLI pager
export GH_PAGER=""
export PAGER=""

echo "🎯 Creating Week 1 Issues from JSON"
echo "==================================="

# Check if JSON file exists
if [[ ! -f ".github/issues/issues.json" ]]; then
    echo "❌ JSON file not found. Please run parse-issues.py first."
    exit 1
fi

# Extract and create Week 1 issues
echo "📝 Extracting Week 1 issues..."

python3 -c "
import json

# Load the issues
with open('.github/issues/issues.json', 'r') as f:
    data = json.load(f)

# Filter Week 1 issues
week1_issues = []
for issue in data['issues']:
    labels = issue.get('labels', [])
    if 'week-1' in labels:
        week1_issues.append(issue)

print(f'Found {len(week1_issues)} Week 1 issues')

# Create issues
for i, issue in enumerate(week1_issues, 1):
    print(f'\\n=== Issue {i}/{len(week1_issues)}: {issue[\"id\"]} ===')
    print(f'Title: {issue[\"title\"]}')
    print(f'Labels: {\", \".join(issue.get(\"labels\", []))}')
    print(f'Assignee: {issue.get(\"assignee\", \"none\")}')
    
    # Prepare data for shell script
    title = issue['title'].replace('\"', '\\\"')
    body = issue.get('body', '').replace('\"', '\\\"').replace('\\n', ' ')[:500] + '...'
    labels = ','.join(issue.get('labels', []))
    assignee = issue.get('assignee', '').replace('@', '')
    
    if assignee == 'me':
        assignee = 'ndethi'
    
    print(f'Cleaned assignee: {assignee}')
    print(f'Cleaned labels: {labels}')
    
    # Write shell command to a temp file
    cmd = f'gh issue create --title \"{title}\" --body \"{body}\" --label \"{labels}\"'
    if assignee:
        cmd += f' --assignee \"{assignee}\"'
    
    print(f'Command: {cmd}')
    
    # Execute the command
    import subprocess
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f'✅ Successfully created issue: {issue[\"id\"]}')
            print(f'   URL: {result.stdout.strip()}')
        else:
            print(f'❌ Failed to create issue: {issue[\"id\"]}')
            print(f'   Error: {result.stderr.strip()}')
    except Exception as e:
        print(f'❌ Exception creating issue: {e}')
    
    # Rate limiting
    import time
    time.sleep(2)

print(f'\\n🎉 Week 1 issue creation process completed!')
"

echo ""
echo "📋 Current issues in repository:"
gh issue list --limit 10
