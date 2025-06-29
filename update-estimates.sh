#!/bin/bash

# Time Estimation Update Utility
# Updates time estimates and actual hours for issues

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
CONSOLIDATED_FILE="$SCRIPT_DIR/.github/issues/consolidated-issues.md"
BACKUP_DIR="$SCRIPT_DIR/.github/issues/backups"
LOG_FILE="$SCRIPT_DIR/estimation-updates.log"

# Default settings
INTERACTIVE_MODE=true
BACKUP_ENABLED=true
VERBOSE=false

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

print_help() {
    cat << EOF
Time Estimation Update Utility
Updates time estimates and actual hours for issues

USAGE:
    $0 [OPTIONS] [COMMAND]

COMMANDS:
    update ISSUE_ID         Update estimates for specific issue
    batch                   Batch update multiple issues
    report                  Generate estimation accuracy report
    sync                    Sync estimates with GitHub (if available)

OPTIONS:
    --non-interactive       Run in non-interactive mode
    --no-backup            Disable backup creation
    --estimated-hours H     Set estimated hours for issue
    --actual-hours H        Set actual hours spent
    --remaining-hours H     Set remaining hours estimate
    --completion-percent P  Set completion percentage
    -v, --verbose          Enable verbose output
    -h, --help             Show this help message

EXAMPLES:
    # Interactive update for issue
    $0 update ISSUE_001

    # Set specific estimates
    $0 update ISSUE_001 --estimated-hours 8 --actual-hours 6 --remaining-hours 2

    # Batch update mode
    $0 batch

    # Generate estimation report
    $0 report

    # Update completion percentage
    $0 update ISSUE_001 --completion-percent 75

ESTIMATION FIELDS:
    - Estimated Hours: Initial time estimate
    - Actual Hours: Time actually spent
    - Remaining Hours: Time remaining to complete
    - Completion %: Percentage of work completed

EOF
}

# Parse command line arguments
parse_args() {
    COMMAND=""
    ISSUE_ID=""
    ESTIMATED_HOURS=""
    ACTUAL_HOURS=""
    REMAINING_HOURS=""
    COMPLETION_PERCENT=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            update|batch|report|sync)
                COMMAND="$1"
                if [[ "$COMMAND" == "update" && -n "$2" && ! "$2" =~ ^-- ]]; then
                    ISSUE_ID="$2"
                    shift
                fi
                shift
                ;;
            --non-interactive)
                INTERACTIVE_MODE=false
                shift
                ;;
            --no-backup)
                BACKUP_ENABLED=false
                shift
                ;;
            --estimated-hours)
                ESTIMATED_HOURS="$2"
                shift 2
                ;;
            --actual-hours)
                ACTUAL_HOURS="$2"
                shift 2
                ;;
            --remaining-hours)
                REMAINING_HOURS="$2"
                shift 2
                ;;
            --completion-percent)
                COMPLETION_PERCENT="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            *)
                if [[ -z "$COMMAND" ]]; then
                    COMMAND="update"
                    ISSUE_ID="$1"
                else
                    echo -e "${RED}Error: Unknown option $1${NC}"
                    print_help
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Default command
    if [[ -z "$COMMAND" ]]; then
        COMMAND="update"
    fi
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Python
    if ! python3 -c "import json, re" >/dev/null 2>&1; then
        log "ERROR: Python 3 with required modules not available."
        exit 1
    fi
    
    # Check consolidated issues file
    if [[ ! -f "$CONSOLIDATED_FILE" ]]; then
        log "ERROR: Consolidated issues file not found: $CONSOLIDATED_FILE"
        exit 1
    fi
    
    log "Prerequisites check completed ✓"
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

# Parse current estimates
parse_estimates() {
    python3 - << 'EOF'
import json
import re
import sys

def parse_estimates_from_markdown(file_path):
    """Parse estimation data from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    issues = []
    issue_sections = re.split(r'\n(?=##\s+\w)', content)
    
    for section in issue_sections:
        if not section.strip():
            continue
        
        # Extract issue ID and title
        title_match = re.search(r'\*\*TITLE:\*\*\s*(.+)', section)
        if not title_match:
            continue
        
        title = title_match.group(1).strip()
        
        # Extract issue ID from title or look for ID field
        issue_id = 'Unknown'
        if title.startswith('[') and ']' in title:
            issue_id = title.split(']')[0][1:]
        else:
            id_match = re.search(r'##\s+(\w+)', section)
            if id_match:
                issue_id = id_match.group(1)
        
        # Look for estimation information in the body
        estimated_hours = None
        actual_hours = None
        remaining_hours = None
        completion_percent = None
        
        # Look for estimation patterns
        est_patterns = [
            r'(?:Est|Estimated?):\s*(\d+(?:\.\d+)?)\s*h',
            r'Estimate:\s*(\d+(?:\.\d+)?)\s*hours?',
            r'Time:\s*(\d+(?:\.\d+)?)\s*h',
        ]
        
        for pattern in est_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                estimated_hours = float(match.group(1))
                break
        
        # Look for actual time patterns
        actual_patterns = [
            r'Actual:\s*(\d+(?:\.\d+)?)\s*h',
            r'Spent:\s*(\d+(?:\.\d+)?)\s*hours?',
            r'Time spent:\s*(\d+(?:\.\d+)?)\s*h',
        ]
        
        for pattern in actual_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                actual_hours = float(match.group(1))
                break
        
        # Look for completion percentage
        completion_patterns = [
            r'(\d+)%\s*complete',
            r'Progress:\s*(\d+)%',
            r'Completion:\s*(\d+)%',
        ]
        
        for pattern in completion_patterns:
            match = re.search(pattern, section, re.IGNORECASE)
            if match:
                completion_percent = int(match.group(1))
                break
        
        # Calculate remaining hours if not explicitly stated
        if estimated_hours is not None and actual_hours is not None:
            remaining_hours = max(0, estimated_hours - actual_hours)
        elif estimated_hours is not None and completion_percent is not None:
            remaining_hours = estimated_hours * (100 - completion_percent) / 100
        
        issue_data = {
            'id': issue_id,
            'title': title,
            'estimated_hours': estimated_hours,
            'actual_hours': actual_hours,
            'remaining_hours': remaining_hours,
            'completion_percent': completion_percent,
            'section_content': section
        }
        
        issues.append(issue_data)
    
    return issues

# Parse and save estimates
issues = parse_estimates_from_markdown('$CONSOLIDATED_FILE')

with open('/tmp/current_estimates.json', 'w') as f:
    json.dump(issues, f, indent=2)

print(f"Parsed {len(issues)} issues with estimation data")
EOF
}

# Interactive update for single issue
interactive_update() {
    local issue_id="$1"
    
    # Find the issue
    local issue_data=$(jq --arg id "$issue_id" '.[] | select(.id == $id)' /tmp/current_estimates.json)
    
    if [[ -z "$issue_data" ]]; then
        echo -e "${RED}Error: Issue $issue_id not found${NC}"
        return 1
    fi
    
    local title=$(echo "$issue_data" | jq -r '.title')
    local current_est=$(echo "$issue_data" | jq -r '.estimated_hours // "Not set"')
    local current_actual=$(echo "$issue_data" | jq -r '.actual_hours // "Not set"')
    local current_remaining=$(echo "$issue_data" | jq -r '.remaining_hours // "Not set"')
    local current_completion=$(echo "$issue_data" | jq -r '.completion_percent // "Not set"')
    
    echo -e "${CYAN}Updating estimates for:${NC}"
    echo -e "${BLUE}$title${NC}"
    echo
    echo "Current estimates:"
    echo "  Estimated hours: $current_est"
    echo "  Actual hours: $current_actual"
    echo "  Remaining hours: $current_remaining"
    echo "  Completion: $current_completion%"
    echo
    
    # Get new values
    if [[ -z "$ESTIMATED_HOURS" && "$INTERACTIVE_MODE" == true ]]; then
        read -p "Estimated hours [$current_est]: " ESTIMATED_HOURS
        [[ -z "$ESTIMATED_HOURS" && "$current_est" != "Not set" ]] && ESTIMATED_HOURS="$current_est"
    fi
    
    if [[ -z "$ACTUAL_HOURS" && "$INTERACTIVE_MODE" == true ]]; then
        read -p "Actual hours spent [$current_actual]: " ACTUAL_HOURS
        [[ -z "$ACTUAL_HOURS" && "$current_actual" != "Not set" ]] && ACTUAL_HOURS="$current_actual"
    fi
    
    if [[ -z "$COMPLETION_PERCENT" && "$INTERACTIVE_MODE" == true ]]; then
        read -p "Completion percentage [$current_completion]: " COMPLETION_PERCENT
        [[ -z "$COMPLETION_PERCENT" && "$current_completion" != "Not set" ]] && COMPLETION_PERCENT="$current_completion"
    fi
    
    if [[ -z "$REMAINING_HOURS" && "$INTERACTIVE_MODE" == true ]]; then
        read -p "Remaining hours [$current_remaining]: " REMAINING_HOURS
        [[ -z "$REMAINING_HOURS" && "$current_remaining" != "Not set" ]] && REMAINING_HOURS="$current_remaining"
    fi
    
    # Update the issue
    update_issue_estimates "$issue_id" "$ESTIMATED_HOURS" "$ACTUAL_HOURS" "$REMAINING_HOURS" "$COMPLETION_PERCENT"
}

# Update issue estimates in markdown file
update_issue_estimates() {
    local issue_id="$1"
    local estimated="$2"
    local actual="$3"
    local remaining="$4"
    local completion="$5"
    
    log "Updating estimates for issue $issue_id..."
    
    python3 - << EOF
import re
import json

issue_id = '$issue_id'
estimated = '$estimated' if '$estimated' else None
actual = '$actual' if '$actual' else None
remaining = '$remaining' if '$remaining' else None
completion = '$completion' if '$completion' else None

# Read current file
with open('$CONSOLIDATED_FILE', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the issue section
issue_sections = re.split(r'\n(?=##\s+\w)', content)
updated_sections = []

for section in issue_sections:
    if not section.strip():
        continue
    
    # Check if this is the target issue
    section_id = None
    title_match = re.search(r'\*\*TITLE:\*\*\s*(.+)', section)
    if title_match:
        title = title_match.group(1).strip()
        if title.startswith('[') and ']' in title:
            section_id = title.split(']')[0][1:]
    
    if not section_id:
        id_match = re.search(r'##\s+(\w+)', section)
        if id_match:
            section_id = id_match.group(1)
    
    if section_id == issue_id:
        # Update this section
        updated_section = section
        
        # Add or update estimation section
        estimation_block = "\n### 📊 Time Estimation\n"
        if estimated:
            estimation_block += f"- **Estimated Hours**: {estimated}h\n"
        if actual:
            estimation_block += f"- **Actual Hours**: {actual}h\n"
        if remaining:
            estimation_block += f"- **Remaining Hours**: {remaining}h\n"
        if completion:
            estimation_block += f"- **Completion**: {completion}%\n"
        
        # Remove existing estimation section if present
        updated_section = re.sub(r'\n### 📊 Time Estimation\n.*?(?=\n###|\n---|\n##|\Z)', '', updated_section, flags=re.DOTALL)
        
        # Add new estimation section before the separator or end
        if '\n---\n' in updated_section:
            updated_section = updated_section.replace('\n---\n', estimation_block + '\n---\n', 1)
        else:
            updated_section += estimation_block
        
        updated_sections.append(updated_section)
        print(f"Updated estimates for {issue_id}")
    else:
        updated_sections.append(section)

# Write updated content
updated_content = '\n'.join(updated_sections)
with open('$CONSOLIDATED_FILE', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("File updated successfully")
EOF
    
    echo -e "${GREEN}Estimates updated for issue $issue_id ✓${NC}"
}

# Batch update mode
batch_update() {
    echo -e "${CYAN}Batch Update Mode${NC}"
    echo "This will allow you to update estimates for multiple issues."
    echo
    
    # Parse current estimates
    parse_estimates
    
    # Show issues that need estimates
    echo "Issues available for update:"
    jq -r '.[] | "\(.id): \(.title)"' /tmp/current_estimates.json | nl
    echo
    
    while true; do
        read -p "Enter issue ID to update (or 'done' to finish): " issue_id
        
        if [[ "$issue_id" == "done" || "$issue_id" == "exit" ]]; then
            break
        fi
        
        if [[ -n "$issue_id" ]]; then
            # Clear previous values
            ESTIMATED_HOURS=""
            ACTUAL_HOURS=""
            REMAINING_HOURS=""
            COMPLETION_PERCENT=""
            
            interactive_update "$issue_id"
            echo
        fi
    done
    
    echo -e "${GREEN}Batch update completed ✓${NC}"
}

# Generate estimation accuracy report
generate_report() {
    log "Generating estimation accuracy report..."
    
    parse_estimates
    
    python3 - << 'EOF'
import json
from datetime import datetime

with open('/tmp/current_estimates.json', 'r') as f:
    issues = json.load(f)

print("# Time Estimation Accuracy Report")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Calculate metrics
total_issues = len(issues)
issues_with_estimates = [i for i in issues if i.get('estimated_hours') is not None]
issues_with_actuals = [i for i in issues if i.get('actual_hours') is not None]
completed_issues = [i for i in issues if i.get('completion_percent') == 100]

print("## Summary Statistics")
print(f"- Total Issues: {total_issues}")
print(f"- Issues with Estimates: {len(issues_with_estimates)}")
print(f"- Issues with Actual Time: {len(issues_with_actuals)}")
print(f"- Completed Issues: {len(completed_issues)}")
print()

if issues_with_estimates:
    total_estimated = sum(i['estimated_hours'] for i in issues_with_estimates)
    avg_estimated = total_estimated / len(issues_with_estimates)
    print(f"- Total Estimated Hours: {total_estimated:.1f}h")
    print(f"- Average Estimate: {avg_estimated:.1f}h per issue")

if issues_with_actuals:
    total_actual = sum(i['actual_hours'] for i in issues_with_actuals)
    avg_actual = total_actual / len(issues_with_actuals)
    print(f"- Total Actual Hours: {total_actual:.1f}h")
    print(f"- Average Actual: {avg_actual:.1f}h per issue")

# Estimation accuracy for completed items
accuracy_data = []
for issue in issues:
    if issue.get('estimated_hours') and issue.get('actual_hours'):
        estimated = issue['estimated_hours']
        actual = issue['actual_hours']
        accuracy = min(estimated, actual) / max(estimated, actual) * 100
        variance = ((actual - estimated) / estimated) * 100
        
        accuracy_data.append({
            'id': issue['id'],
            'title': issue['title'],
            'estimated': estimated,
            'actual': actual,
            'accuracy': accuracy,
            'variance': variance
        })

if accuracy_data:
    print("\n## Estimation Accuracy")
    avg_accuracy = sum(d['accuracy'] for d in accuracy_data) / len(accuracy_data)
    print(f"- Average Accuracy: {avg_accuracy:.1f}%")
    
    over_estimates = [d for d in accuracy_data if d['variance'] < -10]  # Over-estimated by >10%
    under_estimates = [d for d in accuracy_data if d['variance'] > 10]  # Under-estimated by >10%
    
    print(f"- Over-estimates (>10%): {len(over_estimates)}")
    print(f"- Under-estimates (>10%): {len(under_estimates)}")
    
    print("\n## Individual Issue Accuracy")
    print("| Issue ID | Title | Estimated | Actual | Accuracy | Variance |")
    print("|----------|-------|-----------|--------|----------|----------|")
    
    for data in sorted(accuracy_data, key=lambda x: x['accuracy']):
        title = data['title'][:30] + "..." if len(data['title']) > 30 else data['title']
        variance_sign = "+" if data['variance'] > 0 else ""
        print(f"| {data['id']} | {title} | {data['estimated']:.1f}h | {data['actual']:.1f}h | {data['accuracy']:.1f}% | {variance_sign}{data['variance']:.1f}% |")

# Issues needing attention
print("\n## Issues Needing Attention")

issues_no_estimates = [i for i in issues if i.get('estimated_hours') is None]
if issues_no_estimates:
    print(f"\n### Missing Estimates ({len(issues_no_estimates)} issues)")
    for issue in issues_no_estimates[:5]:
        print(f"- {issue['id']}: {issue['title']}")
    if len(issues_no_estimates) > 5:
        print(f"... and {len(issues_no_estimates) - 5} more")

issues_no_tracking = [i for i in issues if i.get('estimated_hours') is not None and i.get('actual_hours') is None]
if issues_no_tracking:
    print(f"\n### Missing Time Tracking ({len(issues_no_tracking)} issues)")
    for issue in issues_no_tracking[:5]:
        print(f"- {issue['id']}: {issue['title']}")
    if len(issues_no_tracking) > 5:
        print(f"... and {len(issues_no_tracking) - 5} more")
EOF
}

# Sync with GitHub (if available)
sync_with_github() {
    log "Attempting to sync estimates with GitHub..."
    
    if ! command -v gh >/dev/null 2>&1; then
        echo -e "${YELLOW}GitHub CLI not available - skipping sync${NC}"
        return 0
    fi
    
    if ! gh auth status >/dev/null 2>&1; then
        echo -e "${YELLOW}GitHub CLI not authenticated - skipping sync${NC}"
        return 0
    fi
    
    parse_estimates
    
    echo "Syncing time estimates with GitHub issue comments..."
    
    jq -c '.[] | select(.estimated_hours != null or .actual_hours != null)' /tmp/current_estimates.json | while read -r issue; do
        local issue_id=$(echo "$issue" | jq -r '.id')
        local estimated=$(echo "$issue" | jq -r '.estimated_hours // empty')
        local actual=$(echo "$issue" | jq -r '.actual_hours // empty')
        local completion=$(echo "$issue" | jq -r '.completion_percent // empty')
        
        # Find corresponding GitHub issue (simplified)
        local gh_issue_number=$(gh issue list --search "$issue_id" --json number --jq '.[0].number' 2>/dev/null || echo "")
        
        if [[ -n "$gh_issue_number" ]]; then
            local comment="**Time Tracking Update**\n"
            [[ -n "$estimated" ]] && comment+="- Estimated: ${estimated}h\n"
            [[ -n "$actual" ]] && comment+="- Actual: ${actual}h\n"
            [[ -n "$completion" ]] && comment+="- Completion: ${completion}%\n"
            comment+="\n*Updated by automation script*"
            
            echo "Updating GitHub issue #$gh_issue_number with time estimates..."
            echo -e "$comment" | gh issue comment "$gh_issue_number" --body-file - 2>/dev/null || true
            
            sleep 1  # Rate limiting
        fi
    done
    
    log "GitHub sync completed"
}

# Cleanup temporary files
cleanup() {
    rm -f /tmp/current_estimates.json
}

# Main execution
main() {
    parse_args "$@"
    check_prerequisites
    create_backup
    
    case "$COMMAND" in
        "update")
            if [[ -n "$ISSUE_ID" ]]; then
                parse_estimates
                interactive_update "$ISSUE_ID"
            else
                echo -e "${RED}Error: Issue ID required for update command${NC}"
                print_help
                exit 1
            fi
            ;;
        "batch")
            batch_update
            ;;
        "report")
            generate_report
            ;;
        "sync")
            sync_with_github
            ;;
        *)
            echo -e "${RED}Error: Unknown command $COMMAND${NC}"
            print_help
            exit 1
            ;;
    esac
    
    cleanup
    log "Operation completed successfully"
}

# Trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"
