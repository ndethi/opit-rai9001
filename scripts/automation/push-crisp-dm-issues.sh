#!/bin/bash

# Push CRISP-DM Overview Issues to GitHub
# This script creates GitHub issues from the local CRISP-DM overview files

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Creating CRISP-DM Overview Issues on GitHub...${NC}"

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed or not in PATH${NC}"
    echo "Please install: brew install gh"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with GitHub CLI${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

# Function to extract field from issue file
extract_field() {
    local file="$1"
    local field="$2"
    grep "^**${field}:**" "$file" | sed "s/^**${field}:** *//"
}

# Function to extract body content between ``` markers
extract_body() {
    local file="$1"
    sed -n '/^```$/,/^```$/p' "$file" | sed '1d;$d'
}

# Function to create GitHub issue from local file
create_github_issue() {
    local issue_file="$1"
    local issue_number="$2"
    
    if [[ ! -f "$issue_file" ]]; then
        echo -e "${RED}❌ Issue file not found: $issue_file${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}📝 Processing: $issue_file${NC}"
    
    # Extract metadata
    local title=$(extract_field "$issue_file" "TITLE")
    local labels=$(extract_field "$issue_file" "LABELS")
    local assignee=$(extract_field "$issue_file" "ASSIGNEE")
    local due_date=$(extract_field "$issue_file" "DUE_DATE")
    local body=$(extract_body "$issue_file")
    
    # Clean up assignee (remove @)
    assignee=$(echo "$assignee" | sed 's/@//')
    
    # Add project fields to body
    local project_fields=$(sed -n '/^**PROJECT_FIELDS:**$/,/^$/p' "$issue_file" | sed '1d;$d')
    if [[ -n "$project_fields" ]]; then
        body="$body

## Project Fields
$project_fields"
    fi
    
    echo -e "${BLUE}Creating issue: $title${NC}"
    
    # Create the GitHub issue
    local gh_cmd="gh issue create --title \"$title\" --body \"$body\""
    
    if [[ -n "$labels" ]]; then
        gh_cmd="$gh_cmd --label \"$labels\""
    fi
    
    if [[ -n "$assignee" && "$assignee" != "me" ]]; then
        gh_cmd="$gh_cmd --assignee \"$assignee\""
    fi
    
    echo "Running: $gh_cmd"
    if eval "$gh_cmd"; then
        echo -e "${GREEN}✅ Successfully created issue: $title${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to create issue: $title${NC}"
        return 1
    fi
}

# Create issues in order
issues=(
    ".github/issues/issue-016-crisp-dm-business-understanding-phase.md"
    ".github/issues/issue-017-crisp-dm-data-understanding-phase.md"
    ".github/issues/issue-018-crisp-dm-data-preparation-phase.md"
    ".github/issues/issue-019-crisp-dm-modeling-phase.md"
    ".github/issues/issue-020-crisp-dm-evaluation-phase.md"
    ".github/issues/issue-021-crisp-dm-deployment-phase.md"
)

success_count=0
total_count=${#issues[@]}

echo -e "${BLUE}Creating $total_count CRISP-DM overview issues...${NC}"
echo ""

for i in "${!issues[@]}"; do
    issue_file="${issues[i]}"
    issue_num=$((i + 16))  # Starting from issue 16
    
    echo -e "${BLUE}[$((i + 1))/$total_count]${NC}"
    if create_github_issue "$issue_file" "$issue_num"; then
        ((success_count++))
    fi
    echo ""
    
    # Add a small delay to avoid rate limiting
    sleep 2
done

echo -e "${BLUE}===========================================${NC}"
echo -e "${GREEN}✅ Successfully created: $success_count/$total_count issues${NC}"

if [[ $success_count -eq $total_count ]]; then
    echo -e "${GREEN}🎉 All CRISP-DM overview issues created successfully!${NC}"
    echo ""
    echo -e "${BLUE}📋 Created Issues:${NC}"
    echo "  🎯 Business Understanding Phase Progress"
    echo "  📊 Data Understanding Phase Progress" 
    echo "  🏗️ Data Preparation Phase Progress"
    echo "  🤖 Modeling Phase Progress"
    echo "  ⚖️ Evaluation Phase Progress"
    echo "  🚀 Deployment Phase Progress"
    echo ""
    echo -e "${BLUE}💡 You can view them at: https://github.com/ndethi/opit-rai9001/issues${NC}"
else
    echo -e "${YELLOW}⚠️ Some issues failed to create. Please check the errors above.${NC}"
fi
