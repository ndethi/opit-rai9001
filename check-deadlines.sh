#!/bin/bash

# Deadline Check Utility
# Monitors and alerts for upcoming deadlines and overdue issues

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
CONFIG_FILE="$SCRIPT_DIR/.github-automation-config"
LOG_FILE="$SCRIPT_DIR/deadline-check.log"

# Default settings
ALERT_DAYS=7      # Alert for deadlines within N days
CRITICAL_DAYS=3   # Critical alert for deadlines within N days
SEND_NOTIFICATIONS=false
SLACK_WEBHOOK=""
EMAIL_RECIPIENT=""
VERBOSE=false

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
Deadline Check Utility
Monitors and alerts for upcoming deadlines and overdue issues

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --alert-days DAYS       Days ahead to alert for deadlines (default: 7)
    --critical-days DAYS    Days ahead for critical alerts (default: 3)
    --notify                Enable notifications (Slack/email if configured)
    --slack-webhook URL     Slack webhook URL for notifications
    --email EMAIL           Email address for deadline alerts
    --format FORMAT         Output format: table, json, summary (default: table)
    --only-overdue          Show only overdue issues
    --only-upcoming         Show only upcoming deadlines
    --exclude-completed     Exclude completed issues from alerts
    -v, --verbose           Enable verbose output
    -h, --help              Show this help message

EXAMPLES:
    # Check all deadlines
    $0

    # Alert for deadlines in next 3 days
    $0 --alert-days 3

    # Show only overdue issues
    $0 --only-overdue

    # Send notifications for critical deadlines
    $0 --critical-days 2 --notify

    # Export deadline data as JSON
    $0 --format json > deadlines.json

NOTIFICATION SETUP:
    # Set Slack webhook in config
    echo 'SLACK_WEBHOOK="https://hooks.slack.com/..."' >> .github-automation-config

    # Set email recipient
    echo 'EMAIL_RECIPIENT="you@example.com"' >> .github-automation-config

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --alert-days)
                ALERT_DAYS="$2"
                shift 2
                ;;
            --critical-days)
                CRITICAL_DAYS="$2"
                shift 2
                ;;
            --notify)
                SEND_NOTIFICATIONS=true
                shift
                ;;
            --slack-webhook)
                SLACK_WEBHOOK="$2"
                shift 2
                ;;
            --email)
                EMAIL_RECIPIENT="$2"
                shift 2
                ;;
            --format)
                OUTPUT_FORMAT="$2"
                if [[ ! "$OUTPUT_FORMAT" =~ ^(table|json|summary)$ ]]; then
                    echo -e "${RED}Error: Invalid format. Use: table, json, summary${NC}"
                    exit 1
                fi
                shift 2
                ;;
            --only-overdue)
                FILTER_TYPE="overdue"
                shift
                ;;
            --only-upcoming)
                FILTER_TYPE="upcoming"
                shift
                ;;
            --exclude-completed)
                EXCLUDE_COMPLETED=true
                shift
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
    
    # Check Python
    if ! python3 -c "import json, datetime" >/dev/null 2>&1; then
        log "ERROR: Python 3 with required modules not available."
        exit 1
    fi
    
    # Check consolidated issues file
    if [[ ! -f "$CONSOLIDATED_FILE" ]]; then
        log "ERROR: Consolidated issues file not found: $CONSOLIDATED_FILE"
        exit 1
    fi
    
    # Check notification tools if enabled
    if [[ "$SEND_NOTIFICATIONS" == true ]]; then
        if [[ -n "$SLACK_WEBHOOK" && ! command -v curl >/dev/null 2>&1 ]]; then
            log "WARNING: curl not found. Slack notifications disabled."
            SLACK_WEBHOOK=""
        fi
        
        if [[ -n "$EMAIL_RECIPIENT" && ! command -v mail >/dev/null 2>&1 ]]; then
            log "WARNING: mail command not found. Email notifications disabled."
            EMAIL_RECIPIENT=""
        fi
    fi
    
    log "Prerequisites check completed ✓"
}

# Analyze deadlines
analyze_deadlines() {
    log "Analyzing deadlines..."
    
    python3 - << EOF
import json
import sys
from datetime import datetime, timedelta
import os

# Parse issues
exec(open('$SCRIPT_DIR/parse-issues.py').read().replace('if __name__ == "__main__":', 'if False:'))

parser = IssueParser('$CONSOLIDATED_FILE')
issues = parser.parse_markdown()

now = datetime.now()
alert_days = int(os.environ.get('ALERT_DAYS', '7'))
critical_days = int(os.environ.get('CRITICAL_DAYS', '3'))
exclude_completed = os.environ.get('EXCLUDE_COMPLETED', 'false') == 'true'
filter_type = os.environ.get('FILTER_TYPE', '')

overdue_issues = []
critical_upcoming = []
upcoming_issues = []
no_deadline_issues = []

for issue in issues:
    # Skip completed issues if requested
    if exclude_completed and issue.get('status') == 'completed':
        continue
    
    due_date_str = issue.get('due_date')
    
    if not due_date_str:
        no_deadline_issues.append(issue)
        continue
    
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        days_diff = (due_date - now).days
        
        issue_data = {
            'id': issue.get('id', 'N/A'),
            'title': issue['title'],
            'due_date': due_date_str,
            'status': issue.get('status', 'open'),
            'assignee': issue.get('assignee', 'Unassigned'),
            'labels': issue.get('labels', []),
            'days_diff': days_diff
        }
        
        if days_diff < 0:
            issue_data['days_overdue'] = abs(days_diff)
            overdue_issues.append(issue_data)
        elif days_diff <= critical_days:
            issue_data['days_remaining'] = days_diff
            critical_upcoming.append(issue_data)
        elif days_diff <= alert_days:
            issue_data['days_remaining'] = days_diff
            upcoming_issues.append(issue_data)
            
    except ValueError:
        continue

# Filter based on user request
if filter_type == 'overdue':
    results = {
        'overdue': overdue_issues,
        'critical_upcoming': [],
        'upcoming': [],
        'no_deadline': []
    }
elif filter_type == 'upcoming':
    results = {
        'overdue': [],
        'critical_upcoming': critical_upcoming,
        'upcoming': upcoming_issues,
        'no_deadline': []
    }
else:
    results = {
        'overdue': overdue_issues,
        'critical_upcoming': critical_upcoming,
        'upcoming': upcoming_issues,
        'no_deadline': no_deadline_issues if not exclude_completed else []
    }

# Save results
with open('/tmp/deadline_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

# Print summary
total_alerts = len(overdue_issues) + len(critical_upcoming) + len(upcoming_issues)
print(f"Deadline analysis complete:")
print(f"  Overdue: {len(overdue_issues)}")
print(f"  Critical (≤{critical_days} days): {len(critical_upcoming)}")
print(f"  Upcoming (≤{alert_days} days): {len(upcoming_issues)}")
print(f"  No deadline: {len(no_deadline_issues)}")
print(f"  Total alerts: {total_alerts}")
EOF
    
    log "Deadline analysis completed"
}

# Display results
display_results() {
    local format="${OUTPUT_FORMAT:-table}"
    
    case "$format" in
        "table")
            display_table_format
            ;;
        "json")
            cat /tmp/deadline_analysis.json
            ;;
        "summary")
            display_summary_format
            ;;
    esac
}

# Table format display
display_table_format() {
    python3 - << 'EOF'
import json
from datetime import datetime

with open('/tmp/deadline_analysis.json', 'r') as f:
    data = json.load(f)

def print_section(title, issues, color_code=""):
    if not issues:
        return
    
    print(f"\n{color_code}{title}{chr(27)}[0m")
    print("=" * len(title))
    print(f"{'ID':<15} {'Title':<40} {'Due Date':<12} {'Days':<8} {'Status':<12} {'Assignee':<15}")
    print("-" * 102)
    
    for issue in issues:
        title = issue['title'][:37] + "..." if len(issue['title']) > 40 else issue['title']
        days_info = ""
        
        if 'days_overdue' in issue:
            days_info = f"-{issue['days_overdue']}"
        elif 'days_remaining' in issue:
            days_info = f"+{issue['days_remaining']}"
        
        print(f"{issue['id']:<15} {title:<40} {issue['due_date']:<12} {days_info:<8} {issue['status']:<12} {issue['assignee']:<15}")

# Display sections
print_section("🚨 OVERDUE ISSUES", data['overdue'], "\033[0;31m")
print_section("🔥 CRITICAL UPCOMING (≤3 days)", data['critical_upcoming'], "\033[1;33m")
print_section("⏰ UPCOMING DEADLINES", data['upcoming'], "\033[0;33m")

if data['no_deadline']:
    print_section("📋 ISSUES WITHOUT DEADLINES", data['no_deadline'][:10], "\033[0;36m")
    if len(data['no_deadline']) > 10:
        print(f"\n... and {len(data['no_deadline']) - 10} more issues without deadlines")

print()
EOF
}

# Summary format display
display_summary_format() {
    python3 - << 'EOF'
import json

with open('/tmp/deadline_analysis.json', 'r') as f:
    data = json.load(f)

overdue_count = len(data['overdue'])
critical_count = len(data['critical_upcoming'])
upcoming_count = len(data['upcoming'])
total_alerts = overdue_count + critical_count + upcoming_count

print("📅 DEADLINE SUMMARY")
print("==================")

if total_alerts == 0:
    print("✅ No urgent deadlines or overdue issues!")
else:
    if overdue_count > 0:
        print(f"🚨 {overdue_count} OVERDUE issues require immediate attention")
    
    if critical_count > 0:
        print(f"🔥 {critical_count} issues due within 3 days")
    
    if upcoming_count > 0:
        print(f"⏰ {upcoming_count} issues due within a week")

print(f"\nTotal issues requiring attention: {total_alerts}")

# Show top 3 most urgent
urgent_issues = []
for issue in data['overdue']:
    urgent_issues.append((issue, -issue['days_overdue']))  # Negative for sorting
for issue in data['critical_upcoming']:
    urgent_issues.append((issue, issue['days_remaining']))

if urgent_issues:
    urgent_issues.sort(key=lambda x: x[1])
    print(f"\n🎯 TOP PRIORITIES:")
    for i, (issue, _) in enumerate(urgent_issues[:3], 1):
        if 'days_overdue' in issue:
            urgency = f"{issue['days_overdue']} days overdue"
        else:
            urgency = f"{issue['days_remaining']} days remaining"
        print(f"  {i}. {issue['title']} ({urgency})")
EOF
}

# Send notifications
send_notifications() {
    if [[ "$SEND_NOTIFICATIONS" != true ]]; then
        return 0
    fi
    
    log "Preparing notifications..."
    
    # Get alert counts
    local overdue_count=$(jq '.overdue | length' /tmp/deadline_analysis.json)
    local critical_count=$(jq '.critical_upcoming | length' /tmp/deadline_analysis.json)
    local total_alerts=$((overdue_count + critical_count))
    
    if [[ $total_alerts -eq 0 ]]; then
        log "No urgent deadlines - skipping notifications"
        return 0
    fi
    
    # Send Slack notification
    if [[ -n "$SLACK_WEBHOOK" ]]; then
        send_slack_notification $overdue_count $critical_count
    fi
    
    # Send email notification
    if [[ -n "$EMAIL_RECIPIENT" ]]; then
        send_email_notification $overdue_count $critical_count
    fi
}

# Send Slack notification
send_slack_notification() {
    local overdue_count=$1
    local critical_count=$2
    
    log "Sending Slack notification..."
    
    local color="danger"
    local title="🚨 Deadline Alert"
    local message=""
    
    if [[ $overdue_count -gt 0 ]]; then
        message="$overdue_count overdue issues require immediate attention"
        color="danger"
    elif [[ $critical_count -gt 0 ]]; then
        message="$critical_count issues due within 3 days"
        color="warning"
    fi
    
    # Get top 3 urgent issues for the notification
    local urgent_list=$(python3 - << 'EOF'
import json

with open('/tmp/deadline_analysis.json', 'r') as f:
    data = json.load(f)

urgent = []
for issue in data['overdue'][:2]:
    urgent.append(f"• {issue['title']} ({issue['days_overdue']} days overdue)")
for issue in data['critical_upcoming'][:2]:
    urgent.append(f"• {issue['title']} ({issue['days_remaining']} days remaining)")

print("\\n".join(urgent[:3]))
EOF
)
    
    local payload=$(cat << EOF
{
    "attachments": [
        {
            "color": "$color",
            "title": "$title",
            "text": "$message",
            "fields": [
                {
                    "title": "Most Urgent",
                    "value": "$urgent_list",
                    "short": false
                }
            ],
            "footer": "Issue Management System",
            "ts": $(date +%s)
        }
    ]
}
EOF
)
    
    if curl -s -X POST -H 'Content-type: application/json' --data "$payload" "$SLACK_WEBHOOK" >/dev/null; then
        log "Slack notification sent successfully"
    else
        log "Failed to send Slack notification"
    fi
}

# Send email notification
send_email_notification() {
    local overdue_count=$1
    local critical_count=$2
    
    log "Sending email notification..."
    
    local subject="Deadline Alert: $((overdue_count + critical_count)) issues require attention"
    local body="Deadline Alert Summary

Overdue Issues: $overdue_count
Critical Upcoming: $critical_count

"
    
    # Add urgent issues list
    body+=$(python3 - << 'EOF'
import json

with open('/tmp/deadline_analysis.json', 'r') as f:
    data = json.load(f)

print("OVERDUE ISSUES:")
for issue in data['overdue']:
    print(f"- {issue['title']} (Due: {issue['due_date']}, {issue['days_overdue']} days overdue)")

print("\nCRITICAL UPCOMING:")
for issue in data['critical_upcoming']:
    print(f"- {issue['title']} (Due: {issue['due_date']}, {issue['days_remaining']} days remaining)")
EOF
)
    
    echo "$body" | mail -s "$subject" "$EMAIL_RECIPIENT" 2>/dev/null || log "Failed to send email notification"
}

# Generate exit code based on findings
generate_exit_code() {
    local overdue_count=$(jq '.overdue | length' /tmp/deadline_analysis.json)
    local critical_count=$(jq '.critical_upcoming | length' /tmp/deadline_analysis.json)
    
    if [[ $overdue_count -gt 0 ]]; then
        return 2  # Overdue issues found
    elif [[ $critical_count -gt 0 ]]; then
        return 1  # Critical deadlines found
    else
        return 0  # No urgent issues
    fi
}

# Cleanup temporary files
cleanup() {
    rm -f /tmp/deadline_analysis.json
}

# Main execution
main() {
    # Export variables for Python scripts
    export ALERT_DAYS
    export CRITICAL_DAYS
    export EXCLUDE_COMPLETED
    export FILTER_TYPE
    
    parse_args "$@"
    check_prerequisites
    analyze_deadlines
    display_results
    send_notifications
    cleanup
    
    log "Deadline check completed"
    
    # Generate appropriate exit code
    generate_exit_code
    local exit_code=$?
    
    case $exit_code in
        0) echo -e "${GREEN}No urgent deadlines detected ✓${NC}" ;;
        1) echo -e "${YELLOW}Critical deadlines detected ⚠️${NC}" ;;
        2) echo -e "${RED}Overdue issues require immediate attention! 🚨${NC}" ;;
    esac
    
    exit $exit_code
}

# Trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"
