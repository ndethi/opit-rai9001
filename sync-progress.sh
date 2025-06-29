#!/bin/bash

# Progress Sync Utility
# Synchronizes issue progress between local markdown and GitHub issues

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
LOG_FILE="$SCRIPT_DIR/progress-sync.log"
CONSOLIDATED_FILE="$SCRIPT_DIR/.github/issues/consolidated-issues.md"
BACKUP_DIR="$SCRIPT_DIR/.github/issues/backups"
CONFIG_FILE="$SCRIPT_DIR/.github-automation-config"

# Default settings
DRY_RUN=false
VERBOSE=false
BACKUP_ENABLED=true
DIRECTION="both"  # Options: local-to-github, github-to-local, both

# Progress tracking
declare TOTAL_ISSUES=0
declare SYNCED_ISSUES=0
declare CONFLICTS=0
declare -a CONFLICT_ISSUES=()

# Load configuration
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

print_help() {
    cat << EOF
Progress Sync Utility
Synchronizes issue progress between local markdown and GitHub issues

USAGE:
    $0 [OPTIONS]

OPTIONS:
    -d, --dry-run           Show what would be synced without making changes
    -v, --verbose           Enable verbose output
    -b, --no-backup         Disable backup creation before sync
    --direction DIR         Sync direction: local-to-github, github-to-local, both (default: both)
    --issue-id ID           Sync specific issue only
    --week WEEK             Sync issues from specific week only
    --status STATUS         Sync issues with specific status only
    -h, --help              Show this help message

EXAMPLES:
    # Sync all issues (both directions)
    $0

    # Dry run to preview changes
    $0 --dry-run

    # Sync only from local to GitHub
    $0 --direction local-to-github

    # Sync specific issue
    $0 --issue-id ISSUE_001

    # Sync week 1 issues only
    $0 --week 1

    # Sync only open/in-progress issues
    $0 --status open

PROGRESS SYNC LOGIC:
    1. Fetch current GitHub issue states
    2. Parse local markdown progress
    3. Compare timestamps and completion status
    4. Resolve conflicts (manual intervention if needed)
    5. Apply updates in specified direction

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -b|--no-backup)
                BACKUP_ENABLED=false
                shift
                ;;
            --direction)
                DIRECTION="$2"
                if [[ ! "$DIRECTION" =~ ^(local-to-github|github-to-local|both)$ ]]; then
                    echo -e "${RED}Error: Invalid direction. Use: local-to-github, github-to-local, both${NC}"
                    exit 1
                fi
                shift 2
                ;;
            --issue-id)
                FILTER_ISSUE_ID="$2"
                shift 2
                ;;
            --week)
                FILTER_WEEK="$2"
                shift 2
                ;;
            --status)
                FILTER_STATUS="$2"
                shift 2
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            *)
                echo -e "${RED}Error: Unknown option $1${NC}"
                print_help
                exit 1
                ;;
        esac
    done
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check GitHub CLI
    if ! command -v gh >/dev/null 2>&1; then
        log "ERROR: GitHub CLI (gh) not found. Install it first."
        exit 1
    fi
    
    # Check GitHub authentication
    if ! gh auth status >/dev/null 2>&1; then
        log "ERROR: GitHub CLI not authenticated. Run 'gh auth login' first."
        exit 1
    fi
    
    # Check Python dependencies
    if ! python3 -c "import json, re, datetime" >/dev/null 2>&1; then
        log "ERROR: Required Python modules not available."
        exit 1
    fi
    
    # Check consolidated issues file
    if [[ ! -f "$CONSOLIDATED_FILE" ]]; then
        log "ERROR: Consolidated issues file not found: $CONSOLIDATED_FILE"
        exit 1
    fi
    
    log "Prerequisites check passed ✓"
}

# Create backup
create_backup() {
    if [[ "$BACKUP_ENABLED" == true ]]; then
        log "Creating backup..."
        
        mkdir -p "$BACKUP_DIR"
        local timestamp=$(date '+%Y%m%d_%H%M%S')
        local backup_file="$BACKUP_DIR/consolidated-issues_${timestamp}.md"
        
        cp "$CONSOLIDATED_FILE" "$backup_file"
        log "Backup created: $backup_file"
    fi
}

# Fetch GitHub issue data
fetch_github_issues() {
    log "Fetching GitHub issues..."
    
    local filter_args=""
    [[ -n "$FILTER_STATUS" ]] && filter_args="$filter_args --state $FILTER_STATUS"
    
    # Get issues with labels, assignees, and project fields
    gh issue list $filter_args --json number,title,state,labels,assignees,body,createdAt,updatedAt --limit 1000 > /tmp/github_issues.json
    
    log "Fetched $(jq length /tmp/github_issues.json) GitHub issues"
}

# Parse local markdown progress
parse_local_progress() {
    log "Parsing local markdown progress..."
    
    # Use the existing parse-issues.py script with additional progress tracking
    python3 "$SCRIPT_DIR/parse-issues.py" \
        --file "$CONSOLIDATED_FILE" \
        --output /tmp/local_issues.json \
        --include-progress \
        ${FILTER_WEEK:+--week "$FILTER_WEEK"} \
        ${FILTER_ISSUE_ID:+--issue-id "$FILTER_ISSUE_ID"}
    
    log "Parsed $(jq length /tmp/local_issues.json) local issues"
}

# Compare and identify sync needs
identify_sync_needs() {
    log "Identifying sync requirements..."
    
    python3 - << 'EOF'
import json
import sys
from datetime import datetime

# Load data
with open('/tmp/github_issues.json', 'r') as f:
    github_issues = json.load(f)

with open('/tmp/local_issues.json', 'r') as f:
    local_issues = json.load(f)

# Create lookup maps
github_map = {}
for issue in github_issues:
    # Extract issue ID from title or body
    title = issue['title']
    if title.startswith('[') and ']' in title:
        issue_id = title.split(']')[0][1:]
        github_map[issue_id] = issue

local_map = {issue['id']: issue for issue in local_issues}

sync_actions = []

# Compare each local issue with GitHub
for issue_id, local_issue in local_map.items():
    github_issue = github_map.get(issue_id)
    
    action = {
        'issue_id': issue_id,
        'local_data': local_issue,
        'github_data': github_issue,
        'sync_needed': False,
        'conflict': False,
        'actions': []
    }
    
    if github_issue is None:
        # Issue exists locally but not on GitHub
        action['sync_needed'] = True
        action['actions'].append('create_on_github')
    else:
        # Compare progress and status
        local_progress = local_issue.get('progress', {})
        github_state = github_issue['state']
        
        # Check if completion status differs
        local_completed = local_progress.get('completed_tasks', 0)
        local_total = local_progress.get('total_tasks', 0)
        local_complete = local_completed == local_total and local_total > 0
        github_complete = github_state == 'closed'
        
        if local_complete != github_complete:
            action['sync_needed'] = True
            if local_complete:
                action['actions'].append('close_github_issue')
            else:
                action['actions'].append('reopen_github_issue')
        
        # Check for label differences
        local_labels = set(local_issue.get('labels', []))
        github_labels = set(label['name'] for label in github_issue.get('labels', []))
        
        if local_labels != github_labels:
            action['sync_needed'] = True
            action['actions'].append('update_labels')
        
        # Check for body/description differences
        if local_issue.get('body') != github_issue.get('body'):
            # This could be a conflict - needs manual review
            action['conflict'] = True
            action['actions'].append('resolve_body_conflict')
    
    sync_actions.append(action)

# Save sync plan
with open('/tmp/sync_plan.json', 'w') as f:
    json.dump(sync_actions, f, indent=2)

# Print summary
needs_sync = [a for a in sync_actions if a['sync_needed']]
conflicts = [a for a in sync_actions if a['conflict']]

print(f"Issues needing sync: {len(needs_sync)}")
print(f"Conflicts requiring manual review: {len(conflicts)}")

if conflicts:
    print("\nConflicts:")
    for conflict in conflicts:
        print(f"  - {conflict['issue_id']}: {', '.join(conflict['actions'])}")
EOF
    
    TOTAL_ISSUES=$(jq length /tmp/sync_plan.json)
    local needs_sync=$(jq '[.[] | select(.sync_needed == true)] | length' /tmp/sync_plan.json)
    CONFLICTS=$(jq '[.[] | select(.conflict == true)] | length' /tmp/sync_plan.json)
    
    log "Analysis complete: $needs_sync issues need sync, $CONFLICTS conflicts found"
}

# Execute sync operations
execute_sync() {
    if [[ "$DRY_RUN" == true ]]; then
        log "DRY RUN MODE - Showing planned changes:"
        jq -r '.[] | select(.sync_needed == true) | "\(.issue_id): \(.actions | join(", "))"' /tmp/sync_plan.json
        return 0
    fi
    
    log "Executing sync operations..."
    
    # Process each sync action
    jq -c '.[] | select(.sync_needed == true)' /tmp/sync_plan.json | while read -r action; do
        local issue_id=$(echo "$action" | jq -r '.issue_id')
        local actions=$(echo "$action" | jq -r '.actions[]')
        
        log "Syncing $issue_id..."
        
        for sync_action in $actions; do
            case "$sync_action" in
                "create_on_github")
                    create_github_issue "$action"
                    ;;
                "close_github_issue")
                    close_github_issue "$action"
                    ;;
                "reopen_github_issue")
                    reopen_github_issue "$action"
                    ;;
                "update_labels")
                    update_github_labels "$action"
                    ;;
                "resolve_body_conflict")
                    handle_body_conflict "$action"
                    ;;
            esac
        done
        
        ((SYNCED_ISSUES++))
        
        # Rate limiting
        sleep 0.5
    done
    
    log "Sync complete: $SYNCED_ISSUES issues synced"
}

# Helper functions for sync operations
create_github_issue() {
    local action="$1"
    local issue_data=$(echo "$action" | jq '.local_data')
    local title=$(echo "$issue_data" | jq -r '.title')
    local body=$(echo "$issue_data" | jq -r '.body // ""')
    local labels=$(echo "$issue_data" | jq -r '.labels[]?' | tr '\n' ',' | sed 's/,$//')
    
    log "Creating GitHub issue: $title"
    
    if [[ "$VERBOSE" == true ]]; then
        echo "gh issue create --title \"$title\" --body \"$body\" ${labels:+--label \"$labels\"}"
    fi
    
    gh issue create --title "$title" --body "$body" ${labels:+--label "$labels"}
}

close_github_issue() {
    local action="$1"
    local github_issue=$(echo "$action" | jq '.github_data')
    local issue_number=$(echo "$github_issue" | jq -r '.number')
    
    log "Closing GitHub issue #$issue_number"
    gh issue close "$issue_number" --comment "Closed automatically - all tasks completed"
}

reopen_github_issue() {
    local action="$1"
    local github_issue=$(echo "$action" | jq '.github_data')
    local issue_number=$(echo "$github_issue" | jq -r '.number')
    
    log "Reopening GitHub issue #$issue_number"
    gh issue reopen "$issue_number" --comment "Reopened automatically - incomplete tasks detected"
}

update_github_labels() {
    local action="$1"
    local github_issue=$(echo "$action" | jq '.github_data')
    local local_issue=$(echo "$action" | jq '.local_data')
    local issue_number=$(echo "$github_issue" | jq -r '.number')
    local labels=$(echo "$local_issue" | jq -r '.labels[]?' | tr '\n' ',' | sed 's/,$//')
    
    log "Updating labels for GitHub issue #$issue_number"
    
    # Remove all existing labels and add new ones
    gh issue edit "$issue_number" --remove-label "$(gh issue view "$issue_number" --json labels --jq '.labels[].name' | tr '\n' ',' | sed 's/,$//')" 2>/dev/null || true
    [[ -n "$labels" ]] && gh issue edit "$issue_number" --add-label "$labels"
}

handle_body_conflict() {
    local action="$1"
    local issue_id=$(echo "$action" | jq -r '.issue_id')
    
    log "CONFLICT: Issue $issue_id has conflicting body content"
    echo -e "${YELLOW}Manual review required for issue $issue_id${NC}"
    
    CONFLICT_ISSUES+=("$issue_id")
}

# Show final summary
show_summary() {
    log "=== SYNC SUMMARY ==="
    log "Total issues processed: $TOTAL_ISSUES"
    log "Successfully synced: $SYNCED_ISSUES"
    log "Conflicts requiring manual review: $CONFLICTS"
    
    if [[ ${#CONFLICT_ISSUES[@]} -gt 0 ]]; then
        log "Issues with conflicts:"
        for issue_id in "${CONFLICT_ISSUES[@]}"; do
            log "  - $issue_id"
        done
    fi
    
    if [[ "$CONFLICTS" -gt 0 ]]; then
        echo -e "${YELLOW}Some issues require manual review. Check the log for details.${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Sync completed successfully!${NC}"
}

# Cleanup temporary files
cleanup() {
    rm -f /tmp/github_issues.json /tmp/local_issues.json /tmp/sync_plan.json
}

# Main execution
main() {
    parse_args "$@"
    
    log "Starting progress sync..."
    [[ "$DRY_RUN" == true ]] && log "DRY RUN MODE ENABLED"
    
    check_prerequisites
    create_backup
    fetch_github_issues
    parse_local_progress
    identify_sync_needs
    execute_sync
    show_summary
    cleanup
}

# Trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"
