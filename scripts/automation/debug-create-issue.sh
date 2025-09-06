#!/bin/bash

# Debug script to test issue creation with better error handling
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Testing GitHub issue creation with debug output...${NC}"

# Test 1: Check GitHub CLI authentication
echo -e "\n${YELLOW}Test 1: Checking GitHub CLI authentication...${NC}"
if ! gh auth status 2>/dev/null; then
    echo -e "${RED}❌ GitHub CLI not authenticated${NC}"
    exit 1
else
    echo -e "${GREEN}✅ GitHub CLI authenticated${NC}"
fi

# Test 2: Check repository access
echo -e "\n${YELLOW}Test 2: Checking repository access...${NC}"
if ! gh repo view 2>/dev/null >/dev/null; then
    echo -e "${RED}❌ Cannot access repository${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Repository accessible${NC}"
fi

# Test 3: Simple issue creation test
echo -e "\n${YELLOW}Test 3: Creating a simple test issue...${NC}"

# First, check if we can create issues at all
echo "Checking repository permissions..."
REPO_INFO=$(gh api repos/:owner/:repo 2>/dev/null || echo "{}")
ISSUES_ENABLED=$(echo "$REPO_INFO" | python3 -c "import json,sys; data=json.load(sys.stdin) if sys.stdin.read().strip() else {}; print(data.get('has_issues', False))" 2>/dev/null || echo "false")

if [[ "$ISSUES_ENABLED" != "True" ]]; then
    echo -e "${RED}❌ Issues may not be enabled for this repository${NC}"
    echo "Repository info: $REPO_INFO"
fi

# Create a simple test issue with verbose output
TEST_TITLE="Debug Test Issue $(date +%s)"
TEST_BODY="This is a test issue created to debug the automation script at $(date)"

echo "Creating issue with title: $TEST_TITLE"
echo "Command: gh issue create --title \"$TEST_TITLE\" --body \"$TEST_BODY\" --label \"test\""

# Capture both stdout and stderr
if OUTPUT=$(gh issue create --title "$TEST_TITLE" --body "$TEST_BODY" --label "test" 2>&1); then
    echo -e "${GREEN}✅ Successfully created test issue${NC}"
    echo "Issue URL: $OUTPUT"
    
    # Extract issue number
    ISSUE_NUMBER=$(echo "$OUTPUT" | grep -o '#[0-9]\+' | head -1 | sed 's/#//')
    if [[ -n "$ISSUE_NUMBER" ]]; then
        echo "Issue number: $ISSUE_NUMBER"
        
        # Clean up - close the test issue
        echo -e "\n${YELLOW}Cleaning up test issue...${NC}"
        if gh issue close "$ISSUE_NUMBER" --reason "not_planned" 2>/dev/null; then
            echo -e "${GREEN}✅ Test issue closed${NC}"
        fi
    fi
else
    echo -e "${RED}❌ Failed to create test issue${NC}"
    echo "Error output: $OUTPUT"
    exit 1
fi

# Test 4: Test with parsed issue data
echo -e "\n${YELLOW}Test 4: Testing with sample parsed issue data...${NC}"

# Create a sample issue JSON
SAMPLE_JSON='{
    "id": "DEBUG_TEST",
    "title": "Sample Parsed Issue Test",
    "body": "This is a test issue created from parsed JSON data",
    "assignee": "@me",
    "labels": ["test", "debug"]
}'

echo "Sample JSON:"
echo "$SAMPLE_JSON" | python3 -m json.tool

# Extract data similar to create-issues.sh
ISSUE_ID=$(echo "$SAMPLE_JSON" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('id', ''))")
TITLE=$(echo "$SAMPLE_JSON" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('title', ''))")
BODY=$(echo "$SAMPLE_JSON" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('body', ''))")
ASSIGNEE=$(echo "$SAMPLE_JSON" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('assignee', ''))")
LABELS_JSON=$(echo "$SAMPLE_JSON" | python3 -c "import json, sys; data=json.load(sys.stdin); print(json.dumps(data.get('labels', [])))")

echo "Extracted data:"
echo "  ID: $ISSUE_ID"
echo "  Title: $TITLE"
echo "  Body: $BODY"
echo "  Assignee: $ASSIGNEE"
echo "  Labels JSON: $LABELS_JSON"

# Convert labels to comma-separated
LABELS=$(echo "$LABELS_JSON" | python3 -c "import json, sys; data=json.load(sys.stdin); print(','.join(data))")
echo "  Labels CSV: $LABELS"

# Handle @me assignee
GITHUB_USER=$(gh api user --jq '.login' 2>/dev/null || echo "unknown")
if [[ "$ASSIGNEE" == "@me" ]]; then
    ASSIGNEE_CLEAN="$GITHUB_USER"
else
    ASSIGNEE_CLEAN=$(echo "$ASSIGNEE" | sed 's/^@//')
fi
echo "  GitHub user: $GITHUB_USER"
echo "  Assignee clean: $ASSIGNEE_CLEAN"

# Build and test command
GH_CMD="gh issue create --title \"$TITLE\" --body \"$BODY\" --label \"$LABELS\" --assignee \"$ASSIGNEE_CLEAN\""
echo -e "\n${YELLOW}Command to execute:${NC}"
echo "$GH_CMD"

echo -e "\n${YELLOW}Creating issue from parsed data...${NC}"
if OUTPUT=$(eval "$GH_CMD" 2>&1); then
    echo -e "${GREEN}✅ Successfully created issue from parsed data${NC}"
    echo "Issue URL: $OUTPUT"
    
    # Extract issue number and clean up
    ISSUE_NUMBER=$(echo "$OUTPUT" | grep -o '#[0-9]\+' | head -1 | sed 's/#//')
    if [[ -n "$ISSUE_NUMBER" ]]; then
        echo "Issue number: $ISSUE_NUMBER"
        echo -e "\n${YELLOW}Cleaning up test issue...${NC}"
        if gh issue close "$ISSUE_NUMBER" --reason "not_planned" 2>/dev/null; then
            echo -e "${GREEN}✅ Test issue closed${NC}"
        fi
    fi
else
    echo -e "${RED}❌ Failed to create issue from parsed data${NC}"
    echo "Error output: $OUTPUT"
    
    # Try to identify the specific error
    if echo "$OUTPUT" | grep -i "unauthorized" >/dev/null; then
        echo -e "${RED}Error: Unauthorized - check repository permissions${NC}"
    elif echo "$OUTPUT" | grep -i "not found" >/dev/null; then
        echo -e "${RED}Error: Repository not found or not accessible${NC}"
    elif echo "$OUTPUT" | grep -i "label" >/dev/null; then
        echo -e "${YELLOW}Warning: Issue with labels - trying without labels${NC}"
        GH_CMD_NO_LABELS="gh issue create --title \"$TITLE\" --body \"$BODY\" --assignee \"$ASSIGNEE_CLEAN\""
        if OUTPUT_NO_LABELS=$(eval "$GH_CMD_NO_LABELS" 2>&1); then
            echo -e "${GREEN}✅ Successfully created issue without labels${NC}"
            echo "Issue URL: $OUTPUT_NO_LABELS"
        else
            echo -e "${RED}❌ Failed even without labels: $OUTPUT_NO_LABELS${NC}"
        fi
    fi
fi

echo -e "\n${BLUE}Debug test complete!${NC}"
