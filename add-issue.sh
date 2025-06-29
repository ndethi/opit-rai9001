#!/bin/bash

# Issue Management Script for OPIT RAI9001 Research Project
# This script helps create and manage individual issue markdown files

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ISSUES_DIR=".github/issues"
CONSOLIDATED_FILE="$ISSUES_DIR/consolidated-issues.md"
TEMPLATE_FILE="$ISSUES_DIR/issue-template.md"

# Ensure we're in the project root
if [[ ! -f "ai-smart-commit.sh" ]]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Create issues directory if it doesn't exist
mkdir -p "$ISSUES_DIR"

# Function to show usage
show_usage() {
    echo -e "${BLUE}OPIT RAI9001 Issue Management Tool${NC}"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  create      Create a new issue file with interactive prompts"
    echo "  list        List all existing issues"
    echo "  extract     Extract an issue from consolidated file"
    echo "  status      Update issue status"
    echo "  template    Show/create issue template"
    echo "  search      Search issues by keyword"
    echo "  help        Show this help message"
    echo ""
    echo "Create Command Usage:"
    echo "  $0 create                               # Interactive mode (recommended)"
    echo "  $0 create \"Issue Title\"                 # Quick mode with prompts"
    echo "  $0 create \"Title\" type priority assignee # Legacy mode"
    echo ""
    echo "Interactive Mode Features:"
    echo "  • Title, labels, assignee, due date input"
    echo "  • Multi-line issue description"
    echo "  • Optional project fields (sprint, criticality, deadlines, etc.)"
    echo "  • Follows consolidated-issues.md format"
    echo ""
    echo "Other Examples:"
    echo "  $0 extract 5"
    echo "  $0 status 3 in-progress"
    echo "  $0 list open"
    echo "  $0 search \"algorithm\""
}

# Function to get next issue number
get_next_issue_number() {
    local max_num=0
    
    # Check existing individual files
    for file in "$ISSUES_DIR"/issue-*.md; do
        if [[ -f "$file" ]]; then
            local num=$(basename "$file" | sed 's/issue-\([0-9]*\)-.*/\1/')
            if [[ "$num" =~ ^[0-9]+$ ]] && [[ $num -gt $max_num ]]; then
                max_num=$num
            fi
        fi
    done
    
    # Check consolidated file for highest issue number
    if [[ -f "$CONSOLIDATED_FILE" ]]; then
        local consolidated_max=$(grep -E "^### Issue #[0-9]+" "$CONSOLIDATED_FILE" | \
                               sed 's/.*#\([0-9]*\).*/\1/' | \
                               sort -n | tail -1)
        if [[ "$consolidated_max" =~ ^[0-9]+$ ]] && [[ $consolidated_max -gt $max_num ]]; then
            max_num=$consolidated_max
        fi
    fi
    
    echo $((max_num + 1))
}

# Function to create issue template
create_template() {
    cat > "$TEMPLATE_FILE" << 'EOF'
# Issue #XXX: [Title]

**TITLE:** [Issue title]
**LABELS:** [comma-separated labels: feature,medium,week-1,etc.]
**ASSIGNEE:** [@username]
**DUE_DATE:** YYYY-MM-DD (optional)
**BODY:**
```
[Detailed description of the issue]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Details
[Implementation notes, technical considerations]

## Related Issues
- Related to #XXX
- Blocks #XXX
- Blocked by #XXX

## Files/Components Affected
- `path/to/file.ext`
- `component/module`

## Notes
[Additional notes, research links, references]
```

**PROJECT_FIELDS:** (optional)
- Sprint_Week: [e.g., Week 1 (Jun 20-26)]
- Criticality: [🚨 CRITICAL | 🛑 BLOCKER | ⚠️ HIGH | 📋 MEDIUM | 💡 LOW]
- OPIT_Deadline: [e.g., Examining Committee (Jul 13)]
- Thesis_Section: [e.g., Introduction, Methodology]
- Effort_Hours: [estimated hours]

---

## Metadata
**Created:** YYYY-MM-DD  
**Updated:** YYYY-MM-DD  
**Status:** [open|in-progress|review|closed]  

## Progress Log
### YYYY-MM-DD
- [Initial notes or progress updates]
EOF
    echo -e "${GREEN}Issue template created at $TEMPLATE_FILE${NC}"
    echo -e "${BLUE}Template follows consolidated-issues.md format${NC}"
}

# Function to create a new issue with interactive prompts
create_issue() {
    # If arguments provided, use them (for backward compatibility)
    local provided_title="$1"
    local provided_type="$2"
    local provided_priority="$3"
    local provided_assignee="$4"
    
    echo -e "${BLUE}OPIT RAI9001 Issue Creator${NC}"
    echo "=============================="
    echo ""
    
    # Interactive prompts for all fields
    local title
    if [[ -n "$provided_title" ]]; then
        title="$provided_title"
        echo -e "${GREEN}Title:${NC} $title"
    else
        read -p "Enter issue title: " title
        if [[ -z "$title" ]]; then
            echo -e "${RED}Error: Issue title is required${NC}"
            return 1
        fi
    fi
    
    # Labels input
    local labels
    if [[ -n "$provided_type" && -n "$provided_priority" ]]; then
        labels="$provided_type,$provided_priority"
        echo -e "${GREEN}Labels:${NC} $labels"
    else
        echo ""
        echo "Common label categories:"
        echo "  Types: feature, bug, enhancement, documentation, research, analysis, planning, sprint"
        echo "  Priority: critical, high, medium, low"
        echo "  Status: blocker, urgent, week-1, week-2, etc."
        echo "  Other: admin, forms, thesis-section, milestone"
        read -p "Enter labels (comma-separated): " labels
        if [[ -z "$labels" ]]; then
            labels="feature,medium"
        fi
    fi
    
    # Assignee
    local assignee
    if [[ -n "$provided_assignee" ]]; then
        assignee="$provided_assignee"
        echo -e "${GREEN}Assignee:${NC} @$assignee"
    else
        read -p "Enter assignee (default: @me): " assignee
        if [[ -z "$assignee" ]]; then
            assignee="@me"
        elif [[ ! "$assignee" =~ ^@ ]]; then
            assignee="@$assignee"
        fi
    fi
    
    # Due date
    local due_date
    echo ""
    echo "Due date format: YYYY-MM-DD (e.g., 2025-06-30)"
    read -p "Enter due date (optional): " due_date
    if [[ -n "$due_date" ]]; then
        # Basic date validation
        if [[ ! "$due_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            echo -e "${YELLOW}Warning: Date format should be YYYY-MM-DD${NC}"
        fi
    fi
    
    # Body/Description
    echo ""
    echo "Issue description (press Enter for multi-line input, type 'END' on a new line to finish):"
    local body=""
    local line
    while IFS= read -r line; do
        if [[ "$line" == "END" ]]; then
            break
        fi
        if [[ -n "$body" ]]; then
            body="$body"$'\n'"$line"
        else
            body="$line"
        fi
    done
    
    if [[ -z "$body" ]]; then
        body="[Issue description to be added]"
    fi
    
    # PROJECT_FIELDS (optional)
    echo ""
    echo -e "${BLUE}Optional Project Fields:${NC}"
    
    read -p "Sprint/Week (e.g., Week 1 (Jun 20-26)): " sprint_week
    
    echo "Criticality levels: 🚨 CRITICAL, 🛑 BLOCKER, ⚠️ HIGH, 📋 MEDIUM, 💡 LOW"
    read -p "Criticality: " criticality
    
    read -p "OPIT Deadline (e.g., Examining Committee (Jul 13)): " opit_deadline
    
    read -p "Thesis Section (e.g., Introduction, Methodology): " thesis_section
    
    read -p "Estimated effort hours: " effort_hours
    
    # Generate issue
    local issue_num=$(get_next_issue_number)
    local today=$(date +%Y-%m-%d)
    local filename_title=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
    local issue_file="$ISSUES_DIR/issue-$(printf "%03d" $issue_num)-$filename_title.md"
    
    # Create the issue file in consolidated format
    cat > "$issue_file" << EOF
# Issue #$(printf "%03d" $issue_num): $title

**TITLE:** $title
**LABELS:** $labels
**ASSIGNEE:** $assignee
EOF

    if [[ -n "$due_date" ]]; then
        echo "**DUE_DATE:** $due_date" >> "$issue_file"
    fi
    
    cat >> "$issue_file" << EOF
**BODY:**
\`\`\`
$body
\`\`\`

EOF

    # Add PROJECT_FIELDS if any were provided
    local has_project_fields=false
    if [[ -n "$sprint_week" || -n "$criticality" || -n "$opit_deadline" || -n "$thesis_section" || -n "$effort_hours" ]]; then
        has_project_fields=true
        echo "**PROJECT_FIELDS:**" >> "$issue_file"
        
        [[ -n "$sprint_week" ]] && echo "- Sprint_Week: $sprint_week" >> "$issue_file"
        [[ -n "$criticality" ]] && echo "- Criticality: $criticality" >> "$issue_file"
        [[ -n "$opit_deadline" ]] && echo "- OPIT_Deadline: $opit_deadline" >> "$issue_file"
        [[ -n "$thesis_section" ]] && echo "- Thesis_Section: $thesis_section" >> "$issue_file"
        [[ -n "$effort_hours" ]] && echo "- Effort_Hours: $effort_hours" >> "$issue_file"
    fi
    
    # Add metadata section
    cat >> "$issue_file" << EOF

---

## Metadata
**Created:** $today  
**Updated:** $today  
**Status:** open  

## Progress Log
### $today
- Issue created: $title
EOF
    
    echo ""
    echo -e "${GREEN}✅ Created issue #$(printf "%03d" $issue_num): $title${NC}"
    echo -e "${BLUE}📁 File: $issue_file${NC}"
    
    # Show summary
    echo ""
    echo -e "${BLUE}Issue Summary:${NC}"
    echo "  Title: $title"
    echo "  Labels: $labels"
    echo "  Assignee: $assignee"
    [[ -n "$due_date" ]] && echo "  Due Date: $due_date"
    [[ "$has_project_fields" == true ]] && echo "  Project fields: included"
    
    # Optionally open in editor
    if command -v code >/dev/null 2>&1; then
        echo ""
        read -p "Open in VS Code? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            code "$issue_file"
        fi
    fi
}

# Function to list issues
list_issues() {
    local filter="${1:-all}"
    
    echo -e "${BLUE}OPIT RAI9001 Project Issues${NC}"
    echo "==============================="
    
    # List individual issue files
    for file in "$ISSUES_DIR"/issue-[0-9]*.md; do
        if [[ -f "$file" ]]; then
            local issue_num=$(basename "$file" | sed 's/issue-\([0-9]*\)-.*/\1/')
            local title=$(grep "^# Issue #" "$file" | sed 's/^# Issue #[0-9]*: //')
            
            # Try new format first, then fall back to old format  
            local status="unknown"
            while IFS=: read -r key value; do
                if [[ "$key" =~ Status ]]; then
                    status=$(echo "$value" | sed 's/^ *//;s/ *$//;s/\*\*//g;s/^ *//')
                    break
                fi
            done < "$file"
            [[ -z "$status" || "$status" == "unknown" ]] && status="unknown"
            
            # Extract labels/priority info
            local labels=$(grep "^\*\*LABELS\*\*:" "$file" | sed 's/.*: //')
            local priority=""
            local type=""
            
            if [[ -n "$labels" ]]; then
                # Parse priority and type from labels
                if echo "$labels" | grep -q "critical"; then priority="critical"
                elif echo "$labels" | grep -q "high"; then priority="high"
                elif echo "$labels" | grep -q "medium"; then priority="medium"
                elif echo "$labels" | grep -q "low"; then priority="low"
                fi
                
                if echo "$labels" | grep -q "bug"; then type="bug"
                elif echo "$labels" | grep -q "feature"; then type="feature"
                elif echo "$labels" | grep -q "enhancement"; then type="enhancement"
                elif echo "$labels" | grep -q "documentation"; then type="docs"
                elif echo "$labels" | grep -q "research"; then type="research"
                elif echo "$labels" | grep -q "planning"; then type="planning"
                elif echo "$labels" | grep -q "sprint"; then type="sprint"
                fi
            else
                # Try old format
                priority=$(grep "^\*\*Priority\*\*:" "$file" | sed 's/.*: //')
                type=$(grep "^\*\*Type\*\*:" "$file" | sed 's/.*: //')
            fi
            
            # Get due date if available
            local due_date=$(grep "^\*\*DUE_DATE\*\*:" "$file" | sed 's/.*: //')
            
            # Apply filter
            if [[ "$filter" != "all" ]] && [[ "$status" != "$filter" ]]; then
                continue
            fi
            
            # Color code by priority
            local color=$NC
            case "$priority" in
                "critical") color=$RED ;;
                "high") color=$YELLOW ;;
                "medium") color=$BLUE ;;
                "low") color=$NC ;;
            esac
            
            # Build display line
            local display_line="#$issue_num [$status]"
            [[ -n "$type" ]] && display_line="$display_line [$type]"
            [[ -n "$due_date" ]] && display_line="$display_line [Due: $due_date]"
            display_line="$display_line $title"
            
            echo -e "${color}$display_line${NC}"
        fi
    done
    
    if [[ "$filter" != "all" ]]; then
        echo ""
        echo -e "${BLUE}Showing issues with status: $filter${NC}"
    fi
}

# Function to extract issue from consolidated file
extract_issue() {
    local issue_num="$1"
    
    if [[ -z "$issue_num" ]]; then
        echo -e "${RED}Error: Issue number is required${NC}"
        echo "Usage: $0 extract <issue_number>"
        return 1
    fi
    
    if [[ ! -f "$CONSOLIDATED_FILE" ]]; then
        echo -e "${RED}Error: Consolidated issues file not found${NC}"
        return 1
    fi
    
    # Extract the issue section from consolidated file
    local start_line=$(grep -n "^### Issue #$(printf "%03d" $issue_num):" "$CONSOLIDATED_FILE" | cut -d: -f1)
    
    if [[ -z "$start_line" ]]; then
        echo -e "${RED}Error: Issue #$issue_num not found in consolidated file${NC}"
        return 1
    fi
    
    # Find the end of this issue (next issue or end of section)
    local end_line=$(tail -n +$((start_line + 1)) "$CONSOLIDATED_FILE" | grep -n "^### Issue #" | head -1 | cut -d: -f1)
    if [[ -n "$end_line" ]]; then
        end_line=$((start_line + end_line - 1))
    else
        end_line=$(wc -l < "$CONSOLIDATED_FILE")
    fi
    
    # Extract issue content
    local title=$(sed -n "${start_line}p" "$CONSOLIDATED_FILE" | sed 's/^### Issue #[0-9]*: //')
    local filename_title=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
    local issue_file="$ISSUES_DIR/issue-$(printf "%03d" $issue_num)-$filename_title.md"
    
    # Create individual issue file
    echo "# Issue #$(printf "%03d" $issue_num): $title" > "$issue_file"
    sed -n "$((start_line + 1)),${end_line}p" "$CONSOLIDATED_FILE" | sed 's/^#### /## /' >> "$issue_file"
    
    # Add progress log section
    echo "" >> "$issue_file"
    echo "## Progress Log" >> "$issue_file"
    echo "### $(date +%Y-%m-%d)" >> "$issue_file"
    echo "- Issue extracted from consolidated file" >> "$issue_file"
    
    echo -e "${GREEN}Extracted issue #$issue_num to $issue_file${NC}"
}

# Function to update issue status
update_status() {
    local issue_num="$1"
    local new_status="$2"
    
    if [[ -z "$issue_num" ]] || [[ -z "$new_status" ]]; then
        echo -e "${RED}Error: Issue number and new status are required${NC}"
        echo "Usage: $0 status <issue_number> <new_status>"
        echo "Valid statuses: open, in-progress, review, closed"
        return 1
    fi
    
    # Find the issue file
    local issue_file=$(ls "$ISSUES_DIR"/issue-$(printf "%03d" $issue_num)-*.md 2>/dev/null | head -1)
    
    if [[ ! -f "$issue_file" ]]; then
        echo -e "${RED}Error: Issue #$issue_num file not found${NC}"
        return 1
    fi
    
    # Update status and timestamp
    local today=$(date +%Y-%m-%d)
    sed -i '' "s/^\*\*Status\*\*:.*/\*\*Status\*\*: $new_status/" "$issue_file"
    sed -i '' "s/^\*\*Updated\*\*:.*/\*\*Updated\*\*: $today/" "$issue_file"
    
    # Add to progress log
    echo "### $today" >> "$issue_file"
    echo "- Status updated to: $new_status" >> "$issue_file"
    
    echo -e "${GREEN}Updated issue #$issue_num status to: $new_status${NC}"
}

# Function to search issues
search_issues() {
    local keyword="$1"
    
    if [[ -z "$keyword" ]]; then
        echo -e "${RED}Error: Search keyword is required${NC}"
        echo "Usage: $0 search <keyword>"
        return 1
    fi
    
    echo -e "${BLUE}Searching for: $keyword${NC}"
    echo "=========================="
    
    for file in "$ISSUES_DIR"/issue-*.md; do
        if [[ -f "$file" ]] && grep -qi "$keyword" "$file"; then
            local issue_num=$(basename "$file" | sed 's/issue-\([0-9]*\)-.*/\1/')
            local title=$(grep "^# Issue #" "$file" | sed 's/^# Issue #[0-9]*: //')
            local status=$(grep "^\*\*Status\*\*:" "$file" | sed 's/.*: //')
            
            echo -e "${GREEN}#$issue_num${NC} [$status] $title"
            
            # Show matching lines
            grep -in "$keyword" "$file" | head -3 | while read line; do
                echo -e "  ${YELLOW}→${NC} $line"
            done
            echo ""
        fi
    done
}

# Main command processing
case "${1:-help}" in
    "create")
        create_issue "$2" "$3" "$4" "$5"
        ;;
    "list")
        list_issues "$2"
        ;;
    "extract")
        extract_issue "$2"
        ;;
    "status")
        update_status "$2" "$3"
        ;;
    "template")
        if [[ ! -f "$TEMPLATE_FILE" ]]; then
            create_template
        else
            echo -e "${BLUE}Issue template:${NC}"
            cat "$TEMPLATE_FILE"
        fi
        ;;
    "search")
        search_issues "$2"
        ;;
    "help"|*)
        show_usage
        ;;
esac
