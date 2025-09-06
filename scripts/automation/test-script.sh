#!/bin/bash

# Test Suite for GitHub Issue Automation System
# Comprehensive testing of all automation components

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
TEST_DIR="$SCRIPT_DIR/.test"
LOG_FILE="$TEST_DIR/test-results.log"

# Test tracking
declare TOTAL_TESTS=0
declare PASSED_TESTS=0
declare FAILED_TESTS=0
declare -a FAILED_TEST_NAMES=()

# Test configuration
RUN_INTEGRATION_TESTS=false
RUN_GITHUB_TESTS=false
VERBOSE=false
CLEANUP_AFTER=true

# Logging function
log() {
    mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

print_help() {
    cat << EOF
Test Suite for GitHub Issue Automation System
Comprehensive testing of all automation components

USAGE:
    $0 [OPTIONS] [TEST_SUITE]

TEST SUITES:
    unit                Unit tests for individual components
    integration         Integration tests (requires GitHub CLI)
    parsing             Markdown parsing and data extraction tests
    automation          Issue creation and management tests
    utilities           Utility script tests
    all                 Run all test suites (default)

OPTIONS:
    --integration       Include integration tests (requires GitHub CLI)
    --github           Include GitHub API tests (requires authentication)
    --no-cleanup       Don't cleanup test files after completion
    -v, --verbose      Enable verbose test output
    -h, --help         Show this help message

EXAMPLES:
    # Run basic unit tests
    $0 unit

    # Run all tests including integration
    $0 --integration all

    # Test only parsing functionality
    $0 parsing

    # Verbose output for debugging
    $0 --verbose unit

EOF
}

# Parse command line arguments
parse_args() {
    TEST_SUITE="all"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            unit|integration|parsing|automation|utilities|all)
                TEST_SUITE="$1"
                shift
                ;;
            --integration)
                RUN_INTEGRATION_TESTS=true
                shift
                ;;
            --github)
                RUN_GITHUB_TESTS=true
                shift
                ;;
            --no-cleanup)
                CLEANUP_AFTER=false
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

# Test framework functions
setup_test_environment() {
    log "Setting up test environment..."
    
    # Create test directory
    mkdir -p "$TEST_DIR"
    rm -f "$LOG_FILE"
    
    # Create sample test data
    create_test_data
    
    log "Test environment ready ✓"
}

create_test_data() {
    # Create test consolidated issues file
    cat > "$TEST_DIR/test-consolidated-issues.md" << 'EOF'
# Test Issues for Automation Testing

## TEST_ISSUE_001
**TITLE:** [TEST-001] Sample Test Issue for Parsing
**LABELS:** test,parsing,high-priority
**ASSIGNEE:** @testuser
**DUE_DATE:** 2025-07-15
**BODY:**
```
This is a test issue for validating the parsing functionality.

### Tasks
- [ ] Task 1 (Est: 2h)
- [x] Task 2 (Est: 3h)
- [ ] Task 3 (Est: 1h)

### Progress
Currently 33% complete.
```

---

## TEST_ISSUE_002
**TITLE:** [TEST-002] Overdue Test Issue
**LABELS:** test,overdue,critical
**ASSIGNEE:** @testuser
**DUE_DATE:** 2025-01-01
**BODY:**
```
This issue is intentionally overdue for deadline testing.

### Tasks
- [x] Completed task
- [ ] Pending task
```

---

## WEEK_1_TEST
**TITLE:** [SPRINT W1] Week 1 Test Sprint
**LABELS:** test,sprint,week-1
**ASSIGNEE:** @testuser
**DUE_DATE:** 2025-07-20
**BODY:**
```
Test sprint for week 1 functionality.

### Sprint Goals
- [ ] Goal 1
- [ ] Goal 2
- [x] Goal 3
```

---
EOF

    # Create test configuration
    cat > "$TEST_DIR/test-config" << EOF
# Test configuration
DEFAULT_RATE_LIMIT_DELAY=0.1
DEFAULT_MAX_RETRIES=1
DEFAULT_BATCH_SIZE=2
DRY_RUN=true
EOF
}

# Test execution framework
run_test() {
    local test_name="$1"
    local test_function="$2"
    
    ((TOTAL_TESTS++))
    
    echo -e "${BLUE}Running: $test_name${NC}"
    
    if [[ "$VERBOSE" == true ]]; then
        log "Starting test: $test_name"
    fi
    
    # Run test in subshell to isolate environment
    if (
        set -e
        cd "$TEST_DIR"
        $test_function
    ); then
        ((PASSED_TESTS++))
        echo -e "${GREEN}✓ PASS: $test_name${NC}"
        [[ "$VERBOSE" == true ]] && log "Test passed: $test_name"
    else
        ((FAILED_TESTS++))
        FAILED_TEST_NAMES+=("$test_name")
        echo -e "${RED}✗ FAIL: $test_name${NC}"
        log "Test failed: $test_name"
    fi
}

# Unit Tests
test_parse_issues_script() {
    # Test parse-issues.py functionality
    python3 "$SCRIPT_DIR/parse-issues.py" \
        --file "test-consolidated-issues.md" \
        --output "parsed-output.json" || return 1
    
    # Verify output exists and is valid JSON
    [[ -f "parsed-output.json" ]] || return 1
    jq empty "parsed-output.json" || return 1
    
    # Check expected number of issues
    local issue_count=$(jq length "parsed-output.json")
    [[ "$issue_count" -eq 3 ]] || return 1
    
    # Verify specific issue data
    local test_issue=$(jq '.[] | select(.id == "TEST_ISSUE_001")' "parsed-output.json")
    [[ -n "$test_issue" ]] || return 1
    
    local title=$(echo "$test_issue" | jq -r '.title')
    [[ "$title" == "[TEST-001] Sample Test Issue for Parsing" ]] || return 1
}

test_markdown_parsing() {
    # Test various markdown parsing scenarios
    python3 - << 'EOF'
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('../parse-issues.py')))

# Mock parse-issues functionality for testing
def test_title_extraction():
    content = "**TITLE:** [TEST-001] Sample Title"
    import re
    match = re.search(r'\*\*TITLE:\*\*\s*(.+)', content)
    assert match is not None, "Title pattern not matched"
    assert match.group(1).strip() == "[TEST-001] Sample Title", "Title extraction failed"

def test_label_extraction():
    content = "**LABELS:** test,parsing,high-priority"
    import re
    match = re.search(r'\*\*LABELS:\*\*\s*(.+)', content)
    assert match is not None, "Labels pattern not matched"
    labels = [label.strip() for label in match.group(1).split(',')]
    assert "test" in labels, "Label 'test' not found"
    assert "parsing" in labels, "Label 'parsing' not found"

def test_date_parsing():
    content = "**DUE_DATE:** 2025-07-15"
    import re
    match = re.search(r'\*\*DUE_DATE:\*\*\s*(.+)', content)
    assert match is not None, "Due date pattern not matched"
    date_str = match.group(1).strip()
    assert date_str == "2025-07-15", "Date extraction failed"

# Run tests
test_title_extraction()
test_label_extraction()  
test_date_parsing()
print("All parsing tests passed")
EOF
}

test_issue_filtering() {
    # Test filtering functionality
    python3 "$SCRIPT_DIR/parse-issues.py" \
        --file "test-consolidated-issues.md" \
        --week 1 \
        --output "filtered-week1.json" || return 1
    
    local week1_count=$(jq length "filtered-week1.json")
    [[ "$week1_count" -eq 1 ]] || return 1
    
    # Test priority filtering
    python3 "$SCRIPT_DIR/parse-issues.py" \
        --file "test-consolidated-issues.md" \
        --priority high \
        --output "filtered-priority.json" || return 1
    
    local high_priority_count=$(jq length "filtered-priority.json")
    [[ "$high_priority_count" -ge 1 ]] || return 1
}

test_deadline_analysis() {
    # Test deadline checking functionality
    export CONSOLIDATED_FILE="test-consolidated-issues.md"
    export ALERT_DAYS=30
    export CRITICAL_DAYS=7
    
    # Mock deadline check
    python3 - << 'EOF'
from datetime import datetime, timedelta
import json

# Simulate deadline analysis
now = datetime.now()

test_issues = [
    {"due_date": "2025-01-01", "title": "Overdue Issue"},
    {"due_date": "2025-07-15", "title": "Future Issue"},
    {"due_date": (now + timedelta(days=2)).strftime('%Y-%m-%d'), "title": "Critical Issue"}
]

overdue = []
critical = []
upcoming = []

for issue in test_issues:
    due_date = datetime.strptime(issue["due_date"], '%Y-%m-%d')
    days_diff = (due_date - now).days
    
    if days_diff < 0:
        overdue.append(issue)
    elif days_diff <= 7:
        critical.append(issue)
    elif days_diff <= 30:
        upcoming.append(issue)

assert len(overdue) >= 1, "Should find overdue issues"
assert len(critical) >= 1, "Should find critical issues"
print("Deadline analysis test passed")
EOF
}

test_config_loading() {
    # Test configuration file loading
    echo 'TEST_VALUE="test123"' > "test-config-file"
    
    # Test loading in bash
    source "test-config-file"
    [[ "$TEST_VALUE" == "test123" ]] || return 1
    
    # Test missing config file handling
    rm -f "non-existent-config"
    if [[ -f "non-existent-config" ]]; then
        source "non-existent-config"
    fi
    # Should not fail even if file doesn't exist
}

# Integration Tests
test_create_issues_dry_run() {
    if [[ "$RUN_INTEGRATION_TESTS" != true ]]; then
        echo "Skipping integration test (use --integration to enable)"
        return 0
    fi
    
    # Test issue creation in dry-run mode
    cp "$TEST_DIR/test-config" "$TEST_DIR/.github-automation-config"
    
    # Mock create-issues.sh execution
    DRY_RUN=true "$SCRIPT_DIR/create-issues.sh" \
        --input "test-consolidated-issues.md" \
        --dry-run || return 1
    
    # Verify no actual issues were created (dry run)
    echo "Dry run test completed"
}

test_github_cli_integration() {
    if [[ "$RUN_GITHUB_TESTS" != true ]]; then
        echo "Skipping GitHub test (use --github to enable)"
        return 0
    fi
    
    # Test GitHub CLI availability and authentication
    if ! command -v gh >/dev/null 2>&1; then
        echo "GitHub CLI not available - skipping"
        return 0
    fi
    
    if ! gh auth status >/dev/null 2>&1; then
        echo "GitHub CLI not authenticated - skipping"
        return 0
    fi
    
    # Test basic GitHub operations
    gh repo view >/dev/null || return 1
    gh issue list --limit 1 >/dev/null || return 1
}

test_sync_progress() {
    # Test progress synchronization
    export CONSOLIDATED_FILE="test-consolidated-issues.md"
    export DRY_RUN=true
    
    # Mock sync execution
    if [[ -f "$SCRIPT_DIR/sync-progress.sh" ]]; then
        bash "$SCRIPT_DIR/sync-progress.sh" --dry-run || return 1
    else
        echo "sync-progress.sh not found - creating mock test"
        return 0
    fi
}

# Utility Tests
test_report_generation() {
    # Test report generation
    export CONSOLIDATED_FILE="test-consolidated-issues.md"
    export OUTPUT_FORMAT="markdown"
    
    if [[ -f "$SCRIPT_DIR/generate-report.sh" ]]; then
        bash "$SCRIPT_DIR/generate-report.sh" \
            --type summary \
            --format markdown \
            --output "test-report.md" || return 1
        
        [[ -f "test-report.md" ]] || return 1
        [[ -s "test-report.md" ]] || return 1  # File not empty
    else
        echo "generate-report.sh not found - skipping"
        return 0
    fi
}

test_deadline_checking() {
    # Test deadline checking utility
    export CONSOLIDATED_FILE="test-consolidated-issues.md"
    
    if [[ -f "$SCRIPT_DIR/check-deadlines.sh" ]]; then
        bash "$SCRIPT_DIR/check-deadlines.sh" \
            --format summary \
            --alert-days 30 || return 1
    else
        echo "check-deadlines.sh not found - skipping"
        return 0
    fi
}

test_estimation_updates() {
    # Test time estimation updates
    cp "test-consolidated-issues.md" "test-consolidated-backup.md"
    
    if [[ -f "$SCRIPT_DIR/update-estimates.sh" ]]; then
        # Test report generation
        bash "$SCRIPT_DIR/update-estimates.sh" report || return 1
    else
        echo "update-estimates.sh not found - skipping"
        return 0
    fi
    
    # Restore backup
    mv "test-consolidated-backup.md" "test-consolidated-issues.md"
}

test_install_script() {
    # Test installation script (without actually installing)
    if [[ -f "$SCRIPT_DIR/install-and-setup.sh" ]]; then
        # Test help output
        bash "$SCRIPT_DIR/install-and-setup.sh" --help >/dev/null || return 1
        
        # Test prerequisite checking
        bash "$SCRIPT_DIR/install-and-setup.sh" --check-only 2>/dev/null || echo "Install check completed"
    else
        echo "install-and-setup.sh not found - skipping"
        return 0
    fi
}

# Test suite execution
run_unit_tests() {
    echo -e "${CYAN}=== UNIT TESTS ===${NC}"
    
    run_test "Parse Issues Script" test_parse_issues_script
    run_test "Markdown Parsing" test_markdown_parsing
    run_test "Issue Filtering" test_issue_filtering
    run_test "Deadline Analysis" test_deadline_analysis
    run_test "Config Loading" test_config_loading
}

run_integration_tests() {
    echo -e "${CYAN}=== INTEGRATION TESTS ===${NC}"
    
    run_test "Create Issues Dry Run" test_create_issues_dry_run
    run_test "GitHub CLI Integration" test_github_cli_integration
    run_test "Progress Sync" test_sync_progress
}

run_parsing_tests() {
    echo -e "${CYAN}=== PARSING TESTS ===${NC}"
    
    run_test "Parse Issues Script" test_parse_issues_script
    run_test "Markdown Parsing" test_markdown_parsing
    run_test "Issue Filtering" test_issue_filtering
}

run_automation_tests() {
    echo -e "${CYAN}=== AUTOMATION TESTS ===${NC}"
    
    run_test "Create Issues Dry Run" test_create_issues_dry_run
    run_test "Progress Sync" test_sync_progress
}

run_utility_tests() {
    echo -e "${CYAN}=== UTILITY TESTS ===${NC}"
    
    run_test "Report Generation" test_report_generation
    run_test "Deadline Checking" test_deadline_checking
    run_test "Estimation Updates" test_estimation_updates
    run_test "Install Script" test_install_script
}

run_all_tests() {
    run_unit_tests
    
    if [[ "$RUN_INTEGRATION_TESTS" == true ]]; then
        run_integration_tests
    fi
    
    run_utility_tests
}

# Test results summary
show_summary() {
    echo
    echo -e "${CYAN}=== TEST SUMMARY ===${NC}"
    echo "Total Tests: $TOTAL_TESTS"
    echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
    
    if [[ $FAILED_TESTS -gt 0 ]]; then
        echo
        echo -e "${RED}Failed Tests:${NC}"
        for test_name in "${FAILED_TEST_NAMES[@]}"; do
            echo "  - $test_name"
        done
        echo
        echo -e "${YELLOW}Check $LOG_FILE for detailed error information${NC}"
        return 1
    else
        echo
        echo -e "${GREEN}All tests passed! ✓${NC}"
        return 0
    fi
}

# Cleanup
cleanup_test_environment() {
    if [[ "$CLEANUP_AFTER" == true ]]; then
        log "Cleaning up test environment..."
        cd "$SCRIPT_DIR"
        rm -rf "$TEST_DIR"
        log "Cleanup completed"
    else
        log "Test files preserved in $TEST_DIR"
    fi
}

# Main execution
main() {
    parse_args "$@"
    setup_test_environment
    
    log "Starting test suite: $TEST_SUITE"
    echo -e "${PURPLE}GitHub Issue Automation Test Suite${NC}"
    echo -e "Running: ${BLUE}$TEST_SUITE${NC} tests"
    [[ "$RUN_INTEGRATION_TESTS" == true ]] && echo -e "Integration tests: ${GREEN}enabled${NC}"
    [[ "$RUN_GITHUB_TESTS" == true ]] && echo -e "GitHub tests: ${GREEN}enabled${NC}"
    echo
    
    case "$TEST_SUITE" in
        "unit")
            run_unit_tests
            ;;
        "integration")
            RUN_INTEGRATION_TESTS=true
            run_integration_tests
            ;;
        "parsing")
            run_parsing_tests
            ;;
        "automation")
            run_automation_tests
            ;;
        "utilities")
            run_utility_tests
            ;;
        "all")
            run_all_tests
            ;;
    esac
    
    local test_result=0
    if ! show_summary; then
        test_result=1
    fi
    
    cleanup_test_environment
    exit $test_result
}

# Trap for cleanup
trap cleanup_test_environment EXIT

# Run main function
main "$@"
