#!/bin/bash

# Simple script to create Week 1 issues directly using the parsed JSON data

set -e

# Disable GitHub CLI pager
export GH_PAGER=""
export PAGER=""

echo "🚀 Creating Week 1 Issues Directly"
echo "=================================="

# Generate the JSON file first
echo "📋 Parsing issues from markdown..."
if ! python3 parse-issues.py .github/issues/consolidated-issues.md .github/issues/issues.json; then
    echo "❌ Failed to parse issues"
    exit 1
fi

echo "✅ Issues parsed successfully"

# Extract Week 1 issues
echo "📝 Extracting Week 1 issues..."
WEEK1_ISSUES=$(python3 -c "
import json
with open('.github/issues/issues.json', 'r') as f:
    data = json.load(f)

week1_issues = []
for issue in data['issues']:
    labels = issue.get('labels', [])
    if 'week-1' in labels:
        week1_issues.append(issue)

print(f'Found {len(week1_issues)} Week 1 issues')
for issue in week1_issues:
    print(json.dumps(issue))
")

echo "$WEEK1_ISSUES" | head -1

# Create issues one by one
echo ""
echo "🎯 Creating Week 1 issues..."

issue_count=0
success_count=0

echo "$WEEK1_ISSUES" | tail -n +2 | while IFS= read -r issue_json; do
    if [ -z "$issue_json" ]; then
        continue
    fi
    
    issue_count=$((issue_count + 1))
    
    # Extract issue data
    issue_id=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('id', ''))")
    title=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('title', ''))")
    body=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('body', ''))")
    assignee=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('assignee', ''))")
    labels_json=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(json.dumps(data.get('labels', [])))")
    
    # Convert labels to comma-separated string
    labels=$(echo "$labels_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(','.join(data))")
    
    # Handle @me assignee
    if [[ "$assignee" == "@me" ]]; then
        assignee_clean="ndethi"
    else
        assignee_clean=$(echo "$assignee" | sed 's/^@//')
    fi
    
    echo ""
    echo "📝 Creating issue: $issue_id"
    echo "   Title: $title"
    echo "   Labels: $labels"
    echo "   Assignee: $assignee_clean"
    
    # Build GitHub CLI command
    gh_cmd="gh issue create --title \"$title\" --body \"$body\""
    
    if [[ -n "$labels" ]]; then
        gh_cmd="$gh_cmd --label \"$labels\""
    fi
    
    if [[ -n "$assignee_clean" ]]; then
        gh_cmd="$gh_cmd --assignee \"$assignee_clean\""
    fi
    
    echo "   Command: $gh_cmd"
    
    # Execute command
    if eval "$gh_cmd" >/dev/null 2>&1; then
        echo "   ✅ Successfully created issue $issue_id"
        success_count=$((success_count + 1))
    else
        echo "   ❌ Failed to create issue $issue_id"
        echo "   Trying to get error details..."
        eval "$gh_cmd" 2>&1 | head -3
    fi
    
    # Rate limiting
    sleep 2
done

echo ""
echo "🎉 Week 1 issue creation completed!"
echo "   Total processed: $issue_count"
echo "   Successfully created: $success_count"

# Show current issues
echo ""
echo "📋 Current issues in repository:"
gh issue list --limit 10
