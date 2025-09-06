#!/bin/bash

# GitHub Issue Report Generator
# Generates comprehensive reports on issue progress, deadlines, and project status

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
REPORTS_DIR="$SCRIPT_DIR/reports"
CONFIG_FILE="$SCRIPT_DIR/.github-automation-config"

# Default settings
REPORT_TYPE="summary"
OUTPUT_FORMAT="markdown"
INCLUDE_GITHUB=true
SHOW_CHARTS=false
DATE_RANGE=""

# Load configuration
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

print_help() {
    cat << EOF
GitHub Issue Report Generator
Generates comprehensive reports on issue progress, deadlines, and project status

USAGE:
    $0 [OPTIONS]

OPTIONS:
    -t, --type TYPE         Report type: summary, detailed, weekly, deadlines, progress (default: summary)
    -f, --format FORMAT     Output format: markdown, html, json, csv (default: markdown)
    -o, --output FILE       Output file path (default: auto-generated)
    --no-github             Don't fetch GitHub data (use local only)
    --charts                Include progress charts (requires additional dependencies)
    --week WEEK             Generate report for specific week
    --date-range RANGE      Date range filter (YYYY-MM-DD:YYYY-MM-DD)
    --status STATUS         Filter by issue status
    --priority PRIORITY     Filter by priority level
    -v, --verbose           Enable verbose output
    -h, --help              Show this help message

REPORT TYPES:
    summary         High-level project overview with key metrics
    detailed        Comprehensive issue-by-issue breakdown
    weekly          Week-by-week progress analysis
    deadlines       Upcoming deadlines and overdue items
    progress        Task completion and milestone tracking
    blockers        Issues blocking progress
    velocity        Team velocity and estimation accuracy

OUTPUT FORMATS:
    markdown        GitHub-flavored markdown (default)
    html            Standalone HTML with styling
    json            Machine-readable JSON data
    csv             Spreadsheet-compatible CSV

EXAMPLES:
    # Generate summary report
    $0

    # Weekly progress report in HTML
    $0 --type weekly --format html

    # Deadline report for next 2 weeks
    $0 --type deadlines --date-range $(date +%Y-%m-%d):$(date -d '+14 days' +%Y-%m-%d)

    # Detailed JSON export
    $0 --type detailed --format json --output project-status.json

    # Progress report with charts
    $0 --type progress --charts --format html

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--type)
                REPORT_TYPE="$2"
                if [[ ! "$REPORT_TYPE" =~ ^(summary|detailed|weekly|deadlines|progress|blockers|velocity)$ ]]; then
                    echo -e "${RED}Error: Invalid report type${NC}"
                    exit 1
                fi
                shift 2
                ;;
            -f|--format)
                OUTPUT_FORMAT="$2"
                if [[ ! "$OUTPUT_FORMAT" =~ ^(markdown|html|json|csv)$ ]]; then
                    echo -e "${RED}Error: Invalid output format${NC}"
                    exit 1
                fi
                shift 2
                ;;
            -o|--output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --no-github)
                INCLUDE_GITHUB=false
                shift
                ;;
            --charts)
                SHOW_CHARTS=true
                shift
                ;;
            --week)
                FILTER_WEEK="$2"
                shift 2
                ;;
            --date-range)
                DATE_RANGE="$2"
                shift 2
                ;;
            --status)
                FILTER_STATUS="$2"
                shift 2
                ;;
            --priority)
                FILTER_PRIORITY="$2"
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
    
    # Check Python dependencies
    if ! python3 -c "import json, re, datetime" >/dev/null 2>&1; then
        log "ERROR: Required Python modules not available."
        exit 1
    fi
    
    # Check for charts dependencies if needed
    if [[ "$SHOW_CHARTS" == true ]]; then
        if ! python3 -c "import matplotlib, plotly" >/dev/null 2>&1; then
            log "WARNING: Chart dependencies not available. Install matplotlib and plotly for chart support."
            SHOW_CHARTS=false
        fi
    fi
    
    # Check GitHub CLI if needed
    if [[ "$INCLUDE_GITHUB" == true ]]; then
        if ! command -v gh >/dev/null 2>&1; then
            log "WARNING: GitHub CLI not found. Using local data only."
            INCLUDE_GITHUB=false
        elif ! gh auth status >/dev/null 2>&1; then
            log "WARNING: GitHub CLI not authenticated. Using local data only."
            INCLUDE_GITHUB=false
        fi
    fi
    
    # Check consolidated issues file
    if [[ ! -f "$CONSOLIDATED_FILE" ]]; then
        log "ERROR: Consolidated issues file not found: $CONSOLIDATED_FILE"
        exit 1
    fi
    
    mkdir -p "$REPORTS_DIR"
    log "Prerequisites check completed ✓"
}

# Collect data
collect_data() {
    log "Collecting data for report generation..."
    
    # Parse local issues
    local parse_args="--file '$CONSOLIDATED_FILE' --output /tmp/local_issues.json --include-progress"
    [[ -n "$FILTER_WEEK" ]] && parse_args="$parse_args --week '$FILTER_WEEK'"
    [[ -n "$FILTER_STATUS" ]] && parse_args="$parse_args --status '$FILTER_STATUS'"
    [[ -n "$FILTER_PRIORITY" ]] && parse_args="$parse_args --priority '$FILTER_PRIORITY'"
    
    eval "python3 '$SCRIPT_DIR/parse-issues.py' $parse_args"
    
    # Fetch GitHub data if enabled
    if [[ "$INCLUDE_GITHUB" == true ]]; then
        log "Fetching GitHub issues..."
        gh issue list --json number,title,state,labels,assignees,body,createdAt,updatedAt,milestone --limit 1000 > /tmp/github_issues.json
    else
        echo "[]" > /tmp/github_issues.json
    fi
    
    log "Data collection completed"
}

# Generate report based on type
generate_report() {
    log "Generating $REPORT_TYPE report in $OUTPUT_FORMAT format..."
    
    case "$REPORT_TYPE" in
        "summary")
            generate_summary_report
            ;;
        "detailed")
            generate_detailed_report
            ;;
        "weekly")
            generate_weekly_report
            ;;
        "deadlines")
            generate_deadlines_report
            ;;
        "progress")
            generate_progress_report
            ;;
        "blockers")
            generate_blockers_report
            ;;
        "velocity")
            generate_velocity_report
            ;;
    esac
}

# Summary report
generate_summary_report() {
    python3 - << 'EOF'
import json
import sys
from datetime import datetime, timedelta
import os

# Load data
with open('/tmp/local_issues.json', 'r') as f:
    local_issues = json.load(f)

with open('/tmp/github_issues.json', 'r') as f:
    github_issues = json.load(f)

output_format = os.environ.get('OUTPUT_FORMAT', 'markdown')

# Calculate metrics
total_issues = len(local_issues)
completed_issues = sum(1 for issue in local_issues if issue.get('status') == 'completed')
in_progress_issues = sum(1 for issue in local_issues if issue.get('status') == 'in-progress')
blocked_issues = sum(1 for issue in local_issues if 'blocked' in issue.get('labels', []))

# Calculate overall progress
total_tasks = sum(issue.get('progress', {}).get('total_tasks', 0) for issue in local_issues)
completed_tasks = sum(issue.get('progress', {}).get('completed_tasks', 0) for issue in local_issues)
progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

# Upcoming deadlines (next 7 days)
now = datetime.now()
upcoming_deadlines = []
for issue in local_issues:
    due_date_str = issue.get('due_date')
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            if now <= due_date <= now + timedelta(days=7):
                upcoming_deadlines.append({
                    'title': issue['title'],
                    'due_date': due_date_str,
                    'days_remaining': (due_date - now).days
                })
        except:
            pass

# Overdue issues
overdue_issues = []
for issue in local_issues:
    due_date_str = issue.get('due_date')
    if due_date_str and issue.get('status') != 'completed':
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            if due_date < now:
                overdue_issues.append({
                    'title': issue['title'],
                    'due_date': due_date_str,
                    'days_overdue': (now - due_date).days
                })
        except:
            pass

# Generate report
if output_format == 'markdown':
    report = f"""# Project Status Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Key Metrics
- **Total Issues**: {total_issues}
- **Completed**: {completed_issues} ({completed_issues/total_issues*100:.1f}%)
- **In Progress**: {in_progress_issues} ({in_progress_issues/total_issues*100:.1f}%)
- **Blocked**: {blocked_issues} ({blocked_issues/total_issues*100:.1f}% if total_issues > 0 else 0)

## 📈 Overall Progress
- **Tasks Completed**: {completed_tasks}/{total_tasks} ({progress_percentage:.1f}%)
- **Progress Bar**: {'█' * int(progress_percentage/5)}{'░' * (20-int(progress_percentage/5))} {progress_percentage:.1f}%

## ⏰ Upcoming Deadlines (Next 7 Days)
"""
    
    if upcoming_deadlines:
        for deadline in sorted(upcoming_deadlines, key=lambda x: x['days_remaining']):
            report += f"- **{deadline['title']}** - Due: {deadline['due_date']} ({deadline['days_remaining']} days)\n"
    else:
        report += "No upcoming deadlines in the next 7 days.\n"
    
    report += "\n## 🚨 Overdue Issues\n"
    
    if overdue_issues:
        for overdue in sorted(overdue_issues, key=lambda x: x['days_overdue'], reverse=True):
            report += f"- **{overdue['title']}** - Due: {overdue['due_date']} ({overdue['days_overdue']} days overdue)\n"
    else:
        report += "No overdue issues.\n"
    
    # Week-by-week breakdown
    report += "\n## 📅 Week-by-Week Status\n"
    weeks = {}
    for issue in local_issues:
        week = 'Unknown'
        for label in issue.get('labels', []):
            if label.startswith('week-'):
                week = label
                break
        
        if week not in weeks:
            weeks[week] = {'total': 0, 'completed': 0}
        weeks[week]['total'] += 1
        if issue.get('status') == 'completed':
            weeks[week]['completed'] += 1
    
    for week in sorted(weeks.keys()):
        if week == 'Unknown':
            continue
        data = weeks[week]
        percentage = (data['completed'] / data['total'] * 100) if data['total'] > 0 else 0
        report += f"- **{week.replace('-', ' ').title()}**: {data['completed']}/{data['total']} ({percentage:.1f}%)\n"

elif output_format == 'json':
    report = json.dumps({
        'generated_at': datetime.now().isoformat(),
        'metrics': {
            'total_issues': total_issues,
            'completed_issues': completed_issues,
            'in_progress_issues': in_progress_issues,
            'blocked_issues': blocked_issues,
            'overall_progress': progress_percentage,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks
        },
        'upcoming_deadlines': upcoming_deadlines,
        'overdue_issues': overdue_issues
    }, indent=2)

elif output_format == 'html':
    report = f"""<!DOCTYPE html>
<html>
<head>
    <title>Project Status Summary</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .metric {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .progress-bar {{ width: 100%; height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); transition: width 0.3s; }}
        .overdue {{ color: #f44336; }}
        .upcoming {{ color: #ff9800; }}
        .completed {{ color: #4CAF50; }}
    </style>
</head>
<body>
    <h1>📊 Project Status Summary</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="metric">
        <h2>Key Metrics</h2>
        <p><strong>Total Issues:</strong> {total_issues}</p>
        <p><strong>Completed:</strong> <span class="completed">{completed_issues} ({completed_issues/total_issues*100:.1f}%)</span></p>
        <p><strong>In Progress:</strong> {in_progress_issues} ({in_progress_issues/total_issues*100:.1f}%)</p>
        <p><strong>Blocked:</strong> {blocked_issues} ({blocked_issues/total_issues*100:.1f}%)</p>
    </div>
    
    <div class="metric">
        <h2>Overall Progress</h2>
        <p><strong>Tasks:</strong> {completed_tasks}/{total_tasks} ({progress_percentage:.1f}%)</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percentage}%"></div>
        </div>
    </div>
</body>
</html>"""

print(report)
EOF
}

# Detailed report (similar structure, but with full issue breakdown)
generate_detailed_report() {
    python3 - << 'EOF'
import json
from datetime import datetime
import os

with open('/tmp/local_issues.json', 'r') as f:
    issues = json.load(f)

output_format = os.environ.get('OUTPUT_FORMAT', 'markdown')

if output_format == 'markdown':
    report = f"""# Detailed Project Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## All Issues Status

"""
    
    for issue in issues:
        status_emoji = {
            'completed': '✅',
            'in-progress': '🔄', 
            'open': '📋',
            'blocked': '⚠️'
        }.get(issue.get('status', 'open'), '📋')
        
        progress = issue.get('progress', {})
        completed_tasks = progress.get('completed_tasks', 0)
        total_tasks = progress.get('total_tasks', 0)
        progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        report += f"""### {status_emoji} {issue['title']}
- **ID**: {issue.get('id', 'N/A')}
- **Status**: {issue.get('status', 'open').title()}
- **Labels**: {', '.join(issue.get('labels', []))}
- **Due Date**: {issue.get('due_date', 'Not set')}
- **Progress**: {completed_tasks}/{total_tasks} tasks ({progress_percent:.1f}%)
- **Assignee**: {issue.get('assignee', 'Unassigned')}

{issue.get('body', 'No description available.')}

---

"""

elif output_format == 'json':
    report = json.dumps({
        'generated_at': datetime.now().isoformat(),
        'issues': issues
    }, indent=2)

print(report)
EOF
}

# Weekly report
generate_weekly_report() {
    python3 - << 'EOF'
import json
from datetime import datetime
import os

with open('/tmp/local_issues.json', 'r') as f:
    issues = json.load(f)

output_format = os.environ.get('OUTPUT_FORMAT', 'markdown')

# Group by week
weeks = {}
for issue in issues:
    week = 'Unscheduled'
    for label in issue.get('labels', []):
        if label.startswith('week-'):
            week = label
            break
    
    if week not in weeks:
        weeks[week] = []
    weeks[week].append(issue)

if output_format == 'markdown':
    report = f"""# Weekly Progress Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    for week in sorted(weeks.keys()):
        if week == 'Unscheduled':
            continue
            
        week_issues = weeks[week]
        completed = sum(1 for issue in week_issues if issue.get('status') == 'completed')
        total = len(week_issues)
        percentage = (completed / total * 100) if total > 0 else 0
        
        report += f"""## {week.replace('-', ' ').title()}
**Progress**: {completed}/{total} issues completed ({percentage:.1f}%)

"""
        
        for issue in week_issues:
            status_emoji = {
                'completed': '✅',
                'in-progress': '🔄',
                'open': '📋',
                'blocked': '⚠️'
            }.get(issue.get('status', 'open'), '📋')
            
            report += f"- {status_emoji} **{issue['title']}**"
            if issue.get('due_date'):
                report += f" (Due: {issue['due_date']})"
            report += "\n"
        
        report += "\n"

print(report)
EOF
}

# Deadlines report
generate_deadlines_report() {
    python3 - << 'EOF'
import json
from datetime import datetime, timedelta
import os

with open('/tmp/local_issues.json', 'r') as f:
    issues = json.load(f)

output_format = os.environ.get('OUTPUT_FORMAT', 'markdown')

now = datetime.now()
upcoming = []
overdue = []

for issue in issues:
    due_date_str = issue.get('due_date')
    if due_date_str and issue.get('status') != 'completed':
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            days_diff = (due_date - now).days
            
            if days_diff < 0:
                overdue.append({**issue, 'days_overdue': abs(days_diff)})
            elif days_diff <= 14:  # Next 2 weeks
                upcoming.append({**issue, 'days_remaining': days_diff})
        except:
            pass

if output_format == 'markdown':
    report = f"""# Deadlines Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🚨 Overdue Issues ({len(overdue)} items)

"""
    
    if overdue:
        for issue in sorted(overdue, key=lambda x: x['days_overdue'], reverse=True):
            report += f"- **{issue['title']}** - Due: {issue['due_date']} ({issue['days_overdue']} days overdue)\n"
    else:
        report += "No overdue issues! 🎉\n"
    
    report += f"\n## ⏰ Upcoming Deadlines ({len(upcoming)} items)\n\n"
    
    if upcoming:
        for issue in sorted(upcoming, key=lambda x: x['days_remaining']):
            urgency = "🔴" if issue['days_remaining'] <= 3 else "🟡" if issue['days_remaining'] <= 7 else "🟢"
            report += f"- {urgency} **{issue['title']}** - Due: {issue['due_date']} ({issue['days_remaining']} days)\n"
    else:
        report += "No upcoming deadlines in the next 2 weeks.\n"

print(report)
EOF
}

# Progress report
generate_progress_report() {
    python3 - << 'EOF'
import json
from datetime import datetime
import os

with open('/tmp/local_issues.json', 'r') as f:
    issues = json.load(f)

output_format = os.environ.get('OUTPUT_FORMAT', 'markdown')

# Calculate progress metrics
total_issues = len(issues)
completed_issues = sum(1 for issue in issues if issue.get('status') == 'completed')
in_progress_issues = sum(1 for issue in issues if issue.get('status') == 'in-progress')

total_tasks = sum(issue.get('progress', {}).get('total_tasks', 0) for issue in issues)
completed_tasks = sum(issue.get('progress', {}).get('completed_tasks', 0) for issue in issues)

if output_format == 'markdown':
    report = f"""# Progress Tracking Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Overall Progress
- **Issues**: {completed_issues}/{total_issues} completed ({completed_issues/total_issues*100:.1f}%)
- **Tasks**: {completed_tasks}/{total_tasks} completed ({completed_tasks/total_tasks*100:.1f}% if total_tasks > 0 else 0)

## 📈 Progress by Issue

"""
    
    for issue in issues:
        progress = issue.get('progress', {})
        completed = progress.get('completed_tasks', 0)
        total = progress.get('total_tasks', 0)
        percentage = (completed / total * 100) if total > 0 else 0
        
        # Progress bar
        filled = int(percentage / 5)  # 20 chars for 100%
        bar = '█' * filled + '░' * (20 - filled)
        
        report += f"**{issue['title']}**\n"
        report += f"`{bar}` {percentage:.1f}% ({completed}/{total} tasks)\n\n"

print(report)
EOF
}

# Blockers report
generate_blockers_report() {
    python3 - << 'EOF'
import json
from datetime import datetime
import os

with open('/tmp/local_issues.json', 'r') as f:
    issues = json.load(f)

blocked_issues = [issue for issue in issues if 'blocked' in issue.get('labels', [])]
at_risk_issues = [issue for issue in issues if 'at-risk' in issue.get('labels', [])]

if os.environ.get('OUTPUT_FORMAT') == 'markdown':
    report = f"""# Blockers and Risks Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🚫 Blocked Issues ({len(blocked_issues)} items)

"""
    
    if blocked_issues:
        for issue in blocked_issues:
            report += f"- **{issue['title']}**\n"
            report += f"  - Status: {issue.get('status', 'open').title()}\n"
            report += f"  - Due: {issue.get('due_date', 'Not set')}\n\n"
    else:
        report += "No blocked issues! 🎉\n"
    
    report += f"\n## ⚠️ At-Risk Issues ({len(at_risk_issues)} items)\n\n"
    
    if at_risk_issues:
        for issue in at_risk_issues:
            report += f"- **{issue['title']}**\n"
            report += f"  - Status: {issue.get('status', 'open').title()}\n"
            report += f"  - Due: {issue.get('due_date', 'Not set')}\n\n"
    else:
        report += "No at-risk issues identified.\n"

    print(report)
EOF
}

# Velocity report
generate_velocity_report() {
    python3 - << 'EOF'
import json
from datetime import datetime, timedelta
import os

with open('/tmp/local_issues.json', 'r') as f:
    issues = json.load(f)

# Simulate velocity calculation (would need historical data for real implementation)
completed_this_week = sum(1 for issue in issues if issue.get('status') == 'completed')
total_estimated_hours = sum(issue.get('estimated_hours', 0) for issue in issues)
total_actual_hours = sum(issue.get('actual_hours', 0) for issue in issues if issue.get('actual_hours'))

if os.environ.get('OUTPUT_FORMAT') == 'markdown':
    report = f"""# Velocity and Estimation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🏃 Velocity Metrics
- **Issues Completed This Period**: {completed_this_week}
- **Average Completion Rate**: {completed_this_week/10:.1f} issues/week (estimated)

## ⏱️ Time Estimation Accuracy
- **Total Estimated**: {total_estimated_hours} hours
- **Total Actual**: {total_actual_hours} hours
- **Estimation Accuracy**: {(min(total_estimated_hours, total_actual_hours) / max(total_estimated_hours, total_actual_hours) * 100) if max(total_estimated_hours, total_actual_hours) > 0 else 0:.1f}%

*Note: Velocity tracking requires historical completion data for more accurate metrics.*
"""
    print(report)
EOF
}

# Set output file if not specified
set_output_file() {
    if [[ -z "$OUTPUT_FILE" ]]; then
        local timestamp=$(date '+%Y%m%d_%H%M%S')
        case "$OUTPUT_FORMAT" in
            "markdown") ext="md" ;;
            "html") ext="html" ;;
            "json") ext="json" ;;
            "csv") ext="csv" ;;
        esac
        OUTPUT_FILE="$REPORTS_DIR/${REPORT_TYPE}_report_${timestamp}.${ext}"
    fi
}

# Save report to file
save_report() {
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    
    # Export environment variables for Python scripts
    export OUTPUT_FORMAT
    export FILTER_WEEK
    export FILTER_STATUS
    export FILTER_PRIORITY
    
    generate_report > "$OUTPUT_FILE"
    
    log "Report saved to: $OUTPUT_FILE"
    
    # Show preview if terminal output
    if [[ "$OUTPUT_FORMAT" == "markdown" && -t 1 ]]; then
        echo -e "\n${CYAN}=== REPORT PREVIEW ===${NC}"
        head -30 "$OUTPUT_FILE"
        [[ $(wc -l < "$OUTPUT_FILE") -gt 30 ]] && echo -e "\n${YELLOW}... (truncated, see full report in $OUTPUT_FILE)${NC}"
    fi
}

# Cleanup temporary files
cleanup() {
    rm -f /tmp/local_issues.json /tmp/github_issues.json
}

# Main execution
main() {
    parse_args "$@"
    check_prerequisites
    set_output_file
    collect_data
    save_report
    cleanup
    
    echo -e "${GREEN}Report generation completed successfully!${NC}"
    echo -e "Report saved to: ${BLUE}$OUTPUT_FILE${NC}"
}

# Trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"
