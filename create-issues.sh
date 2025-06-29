#!/bin/bash

# GitHub Issue Creator
# Creates GitHub issues from parsed JSON data using GitHub CLI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/.github-automation-config"
LOG_FILE="$SCRIPT_DIR/issue-automation.log"
TEMP_DIR="$SCRIPT_DIR/.tmp"

# Default settings
DEFAULT_RATE_LIMIT_DELAY=1
DEFAULT_MAX_RETRIES=3
DEFAULT_BATCH_SIZE=10
DRY_RUN=false
VERBOSE=false

# Load configuration if it exists
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Progress tracking
declare TOTAL_ISSUES=0
declare PROCESSED_ISSUES=0
declare SUCCESSFUL_ISSUES=0
declare FAILED_ISSUES=0
declare -a FAILED_ISSUE_IDS=()

# Show progress
show_progress() {
    local percentage=$((PROCESSED_ISSUES * 100 / TOTAL_ISSUES))
    local bar_length=50
    local filled_length=$((percentage * bar_length / 100))
    
    printf "\r["
    printf "%*s" $filled_length | tr ' ' '='
    printf "%*s" $((bar_length - filled_length)) | tr ' ' '-'
    printf "] %d%% (%d/%d) Success: %d, Failed: %d" \
           $percentage $PROCESSED_ISSUES $TOTAL_ISSUES $SUCCESSFUL_ISSUES $FAILED_ISSUES
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if GitHub CLI is installed
    if ! command -v gh >/dev/null 2>&1; then
        echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
        echo "Please run ./install-and-setup.sh first"
        exit 1
    fi
    
    # Check if authenticated
    if ! gh auth status >/dev/null 2>&1; then
        echo -e "${RED}❌ Not authenticated with GitHub${NC}"
        echo "Please run: gh auth login"
        exit 1
    fi
    
    # Check if Python is available
    if ! command -v python3 >/dev/null 2>&1; then
        echo -e "${RED}❌ Python 3 is required${NC}"
        exit 1
    fi
    
    # Check if repository is configured
    if [[ -f "$SCRIPT_DIR/.repository" ]]; then
        GITHUB_REPO=$(cat "$SCRIPT_DIR/.repository")
    fi
    
    if [[ -z "$GITHUB_REPO" ]]; then
        echo -e "${RED}❌ GitHub repository not configured${NC}"
        echo "Please run ./install-and-setup.sh first"
        exit 1
    fi
    
    # Verify repository access
    if ! gh repo view "$GITHUB_REPO" >/dev/null 2>&1; then
        echo -e "${RED}❌ Cannot access repository: $GITHUB_REPO${NC}"
        exit 1
    fi
    
    log "Prerequisites check passed"
}

# Parse issues from markdown
parse_issues() {
    local input_file="$1"
    local filter_args="$2"
    local output_file="$TEMP_DIR/parsed-issues.json"
    
    log "Parsing issues from: $input_file"
    
    mkdir -p "$TEMP_DIR"
    
    # Run the Python parser
    local parse_cmd="python3 \"$SCRIPT_DIR/parse-issues.py\" \"$input_file\" -o \"$output_file\""
    
    if [[ -n "$filter_args" ]]; then
        parse_cmd="$parse_cmd $filter_args"
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        parse_cmd="$parse_cmd --verbose"
    fi
    
    if eval "$parse_cmd"; then
        echo "$output_file"
        return 0
    else
        echo -e "${RED}❌ Failed to parse issues${NC}"
        exit 1
    fi
}

# Preview issues
preview_issues() {
    local json_file="$1"
    
    echo -e "${BLUE}📋 Issue Preview${NC}"
    echo "================"
    
    # Extract issue count
    local count=$(python3 -c "
import json
with open('$json_file', 'r') as f:
    data = json.load(f)
print(data['metadata']['total_issues'])
")
    
    echo -e "${CYAN}Total issues to create: $count${NC}"
    echo ""
    
    # Show first 5 issues in detail
    python3 -c "
import json
with open('$json_file', 'r') as f:
    data = json.load(f)

for i, issue in enumerate(data['issues'][:5]):
    print(f'Issue #{i+1}: {issue[\"id\"]}')
    print(f'Title: {issue[\"title\"]}')
    print(f'Labels: {\", \".join(issue[\"labels\"])}')
    print(f'Assignee: {issue[\"assignee\"]}')
    if issue['due_date']:
        print(f'Due Date: {issue[\"due_date\"]}')
    print(f'Body Length: {len(issue[\"body\"])} characters')
    if issue['project_fields']:
        print(f'Project Fields: {len(issue[\"project_fields\"])} fields')
    print('-' * 50)

if len(data['issues']) > 5:
    print(f'... and {len(data[\"issues\"]) - 5} more issues')
"
    
    echo ""
    read -p "Do you want to proceed with creating these issues? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled by user"
        exit 0
    fi
}

# Get current GitHub user
get_github_user() {
    gh api user --jq .login
}

# Validate issue data
validate_issue() {
    local issue_json="$1"
    
    # Check required fields
    local title=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('title', ''))")
    
    if [[ -z "$title" ]]; then
        return 1
    fi
    
    return 0
}

# Create a single issue
create_single_issue() {
    local issue_json="$1"
    local attempt=1
    
    # Extract issue data
    local issue_id=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('id', ''))")
    local title=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('title', ''))")
    local body=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('body', ''))")
    local assignee=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('assignee', ''))")
    local labels_json=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(json.dumps(data.get('labels', [])))")
    
    # Handle @me assignee
    if [[ "$assignee" == "@me" ]]; then
        assignee="@$(get_github_user)"
    fi
    
    # Remove @ from assignee for GitHub CLI
    local assignee_clean=$(echo "$assignee" | sed 's/^@//')
    
    # Convert labels array to comma-separated string
    local labels=$(echo "$labels_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(','.join(data))")
    
    if [[ "$DRY_RUN" == true ]]; then
        echo "DRY RUN - Would create issue:"
        echo "  ID: $issue_id"
        echo "  Title: $title"
        echo "  Labels: $labels"
        echo "  Assignee: $assignee_clean"
        echo "  Body length: ${#body} characters"
        return 0
    fi
    
    # Validate issue data
    if ! validate_issue "$issue_json"; then
        log "ERROR: Invalid issue data for $issue_id"
        return 1
    fi
    
    # Retry loop
    while [[ $attempt -le ${MAX_RETRIES:-$DEFAULT_MAX_RETRIES} ]]; do
        if [[ $attempt -gt 1 ]]; then
            log "Retrying issue creation (attempt $attempt): $issue_id"
            sleep $((attempt * 2))  # Exponential backoff
        fi
        
        # Build GitHub CLI command
        local gh_cmd="gh issue create --repo \"$GITHUB_REPO\" --title \"$title\""
        
        if [[ -n "$body" ]]; then
            # Create temporary file for body to handle multiline content
            local body_file="$TEMP_DIR/body-$issue_id.md"
            echo "$body" > "$body_file"
            gh_cmd="$gh_cmd --body-file \"$body_file\""
        fi
        
        if [[ -n "$labels" ]]; then
            gh_cmd="$gh_cmd --label \"$labels\""
        fi
        
        if [[ -n "$assignee_clean" ]]; then
            gh_cmd="$gh_cmd --assignee \"$assignee_clean\""
        fi
        
        # Execute command
        if eval "$gh_cmd" >/dev/null 2>&1; then
            log "SUCCESS: Created issue $issue_id - $title"
            
            # Clean up temporary body file
            [[ -f "$body_file" ]] && rm -f "$body_file"
            
            # Rate limiting
            sleep "${RATE_LIMIT_DELAY:-$DEFAULT_RATE_LIMIT_DELAY}"
            
            return 0
        else
            log "ERROR: Failed to create issue $issue_id (attempt $attempt)"
            attempt=$((attempt + 1))
        fi
    done
    
    log "FAILED: Could not create issue $issue_id after ${MAX_RETRIES:-$DEFAULT_MAX_RETRIES} attempts"
    return 1
}

# Create issues in batches
create_issues_batch() {
    local json_file="$1"
    
    log "Starting batch issue creation from: $json_file"
    
    # Get total count
    TOTAL_ISSUES=$(python3 -c "
import json
with open('$json_file', 'r') as f:
    data = json.load(f)
print(data['metadata']['total_issues'])
")
    
    echo -e "${BLUE}🚀 Creating $TOTAL_ISSUES issues...${NC}"
    echo ""
    
    # Process issues
    python3 -c "
import json
with open('$json_file', 'r') as f:
    data = json.load(f)

for issue in data['issues']:
    print(json.dumps(issue))
" | while IFS= read -r issue_json; do
        PROCESSED_ISSUES=$((PROCESSED_ISSUES + 1))
        
        if create_single_issue "$issue_json"; then
            SUCCESSFUL_ISSUES=$((SUCCESSFUL_ISSUES + 1))
        else
            FAILED_ISSUES=$((FAILED_ISSUES + 1))
            local issue_id=$(echo "$issue_json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('id', 'unknown'))")
            FAILED_ISSUE_IDS+=("$issue_id")
        fi
        
        show_progress
    done
    
    echo ""  # New line after progress bar
}

# Generate summary report
generate_summary() {
    echo ""
    echo -e "${BLUE}📊 Creation Summary${NC}"
    echo "==================="
    echo -e "${GREEN}✅ Successful: $SUCCESSFUL_ISSUES${NC}"
    echo -e "${RED}❌ Failed: $FAILED_ISSUES${NC}"
    echo -e "${CYAN}📊 Total Processed: $PROCESSED_ISSUES${NC}"
    
    if [[ $FAILED_ISSUES -gt 0 ]]; then
        echo ""
        echo -e "${YELLOW}⚠️  Failed Issues:${NC}"
        for failed_id in "${FAILED_ISSUE_IDS[@]}"; do
            echo "  - $failed_id"
        done
        echo ""
        echo "Check the log file for detailed error information: $LOG_FILE"
    fi
    
    echo ""
    echo -e "${CYAN}📁 Repository: https://github.com/$GITHUB_REPO/issues${NC}"
}

# Clean up temporary files
cleanup() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

# Show usage
show_usage() {
    cat << EOF
GitHub Issue Creator

Usage: $0 [OPTIONS]

Options:
  --input FILE         Input markdown file (default: .github/issues/consolidated-issues.md)
  --preview           Preview issues without creating them
  --dry-run           Show what would be created without actually creating
  --week NUMBER       Create issues for specific week (1-10)
  --type TYPE         Create issues of specific type (sprint, milestone, etc.)
  --assignee USER     Create issues for specific assignee
  --priority LEVEL    Create issues with specific priority (critical, high, medium, low)
  --batch-size N      Number of issues to process in parallel (default: 10)
  --rate-limit N      Delay between requests in seconds (default: 1)
  --max-retries N     Maximum retry attempts for failed issues (default: 3)
  --verbose, -v       Verbose output
  --help, -h          Show this help message

Examples:
  $0                                    # Create all issues
  $0 --preview                         # Preview all issues
  $0 --week 1                         # Create week 1 issues only
  $0 --type sprint --dry-run          # Preview sprint issues
  $0 --priority critical              # Create critical priority issues
  $0 --input my-issues.md            # Use custom input file

EOF
}

# Main function
main() {
    local input_file=""
    local preview_mode=false
    local filter_args=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --input)
                input_file="$2"
                shift 2
                ;;
            --preview)
                preview_mode=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --week)
                filter_args="$filter_args --week $2"
                shift 2
                ;;
            --type)
                filter_args="$filter_args --type $2"
                shift 2
                ;;
            --assignee)
                filter_args="$filter_args --assignee $2"
                shift 2
                ;;
            --priority)
                filter_args="$filter_args --priority $2"
                shift 2
                ;;
            --batch-size)
                BATCH_SIZE="$2"
                shift 2
                ;;
            --rate-limit)
                RATE_LIMIT_DELAY="$2"
                shift 2
                ;;
            --max-retries)
                MAX_RETRIES="$2"
                shift 2
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Unknown option: $1${NC}"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Set default input file
    if [[ -z "$input_file" ]]; then
        input_file="$SCRIPT_DIR/.github/issues/consolidated-issues.md"
    fi
    
    # Check if input file exists
    if [[ ! -f "$input_file" ]]; then
        echo -e "${RED}❌ Input file not found: $input_file${NC}"
        exit 1
    fi
    
    echo -e "${PURPLE}🚀 GitHub Issue Creator${NC}"
    echo "========================"
    echo ""
    
    # Setup
    trap cleanup EXIT
    check_prerequisites
    
    # Parse issues
    local json_file
    json_file=$(parse_issues "$input_file" "$filter_args")
    
    # Preview mode
    if [[ "$preview_mode" == true ]]; then
        python3 "$SCRIPT_DIR/parse-issues.py" "$input_file" --preview $filter_args
        exit 0
    fi
    
    # Preview and confirm
    if [[ "$DRY_RUN" != true ]]; then
        preview_issues "$json_file"
    fi
    
    # Create issues
    create_issues_batch "$json_file"
    
    # Generate summary
    generate_summary
    
    log "Issue creation completed"
}

# Run main function
main "$@"
