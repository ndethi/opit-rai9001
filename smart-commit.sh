#!/bin/bash

# thiLLMo Smart Commit Script
# Automates git workflow with AI-assisted commit generation and prompt logging

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DEFAULT_ASSISTANT="GitHub Copilot"
DEFAULT_MODEL="GPT-4"
COMMIT_TEMPLATE_FILE=".commit_template.tmp"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository!"
        exit 1
    fi
}

# Function to check for uncommitted changes
check_changes() {
    if git diff --quiet && git diff --cached --quiet; then
        print_warning "No changes to commit!"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
}

# Function to display current changes
show_changes() {
    print_status "Current changes to be committed:"
    echo
    git status --short
    echo
    
    if [ "$(git diff --cached --name-only | wc -l)" -eq 0 ]; then
        print_status "Staged changes:"
        echo "None"
        echo
        print_status "Unstaged changes:"
        git diff --name-only 2>/dev/null || echo "None"
    else
        print_status "Already staged files:"
        git diff --cached --name-only
        echo
        if [ "$(git diff --name-only | wc -l)" -gt 0 ]; then
            print_status "Unstaged changes:"
            git diff --name-only
        fi
    fi
    echo
}

# Function to auto-stage changes
auto_stage() {
    local stage_all=false
    
    if [ "$(git diff --cached --name-only | wc -l)" -eq 0 ]; then
        print_status "No files staged. Options:"
        echo "1) Stage all changes (git add .)"
        echo "2) Stage specific files"
        echo "3) Skip staging (commit only already staged files)"
        read -p "Choose option (1-3): " -n 1 -r
        echo
        
        case $REPLY in
            1)
                git add .
                print_success "All changes staged"
                ;;
            2)
                print_status "Available files:"
                git status --porcelain | grep -E "^(\?\?|\s*M|\s*A|\s*D)" | cut -c4-
                echo
                read -p "Enter files to stage (space-separated): " files
                if [ -n "$files" ]; then
                    git add $files
                    print_success "Files staged: $files"
                fi
                ;;
            3)
                print_warning "Proceeding with already staged files only"
                ;;
            *)
                print_error "Invalid option"
                exit 1
                ;;
        esac
    else
        print_status "Files already staged:"
        git diff --cached --name-only
        echo
        read -p "Stage additional files? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            auto_stage
        fi
    fi
}

# Function to analyze changes and suggest commit type
suggest_commit_type() {
    local changed_files=$(git diff --cached --name-only)
    local commit_type=""
    
    # Analyze file patterns to suggest commit type
    if echo "$changed_files" | grep -qE "\.(md|txt|rst|tex)$"; then
        if echo "$changed_files" | grep -qE "(README|CHANGELOG|doc/|docs/)"; then
            commit_type="docs"
        fi
    fi
    
    if echo "$changed_files" | grep -qE "\.(py|js|ts|java|cpp|c|go|rs)$"; then
        # Check if it's a new file (feat) or modification (fix/refactor)
        local new_files=$(git diff --cached --diff-filter=A --name-only)
        if [ -n "$new_files" ]; then
            commit_type="feat"
        else
            commit_type="fix"
        fi
    fi
    
    if echo "$changed_files" | grep -qE "\.(json|yaml|yml|toml|cfg|ini)$"; then
        commit_type="chore"
    fi
    
    if echo "$changed_files" | grep -qE "test|spec"; then
        commit_type="test"
    fi
    
    if [ -n "$commit_type" ]; then
        print_status "Suggested commit type: $commit_type"
    fi
    
    echo "$commit_type"
}

# Function to generate smart commit message suggestions
generate_suggestions() {
    local staged_files=$(git diff --cached --name-only)
    local suggestions=()
    
    # Analyze common patterns
    if echo "$staged_files" | grep -q "README\|\.md$"; then
        suggestions+=("Update documentation")
        suggestions+=("Improve project documentation")
    fi
    
    if echo "$staged_files" | grep -qE "\.(py|js|ts)$"; then
        suggestions+=("Implement new functionality")
        suggestions+=("Fix bug in core module")
        suggestions+=("Refactor code structure")
    fi
    
    if echo "$staged_files" | grep -q "\.github/"; then
        suggestions+=("Update GitHub workflows")
        suggestions+=("Improve CI/CD configuration")
    fi
    
    if echo "$staged_files" | grep -qE "(requirements|package\.json|Pipfile)"; then
        suggestions+=("Update dependencies")
        suggestions+=("Add new dependencies")
    fi
    
    # Print suggestions
    if [ ${#suggestions[@]} -gt 0 ]; then
        print_status "Suggested commit messages:"
        for i in "${!suggestions[@]}"; do
            echo "$((i+1)). ${suggestions[$i]}"
        done
        echo
    fi
}

# Function to handle commitizen with pre-filled values
smart_commit() {
    local suggested_type=$(suggest_commit_type)
    
    print_status "Generating commit with AI prompt logging..."
    echo
    
    # Show file changes summary
    print_status "Files being committed:"
    git diff --cached --stat
    echo
    
    # Generate suggestions
    generate_suggestions
    
    # Create temporary commit template with suggestions
    cat > "$COMMIT_TEMPLATE_FILE" << EOF
# Suggested commit type: ${suggested_type:-"feat"}
# 
# Recent changes summary:
$(git diff --cached --stat | head -5)
# 
# Use 'cz commit' format with AI prompt logging
EOF
    
    # Run commitizen
    print_status "Running commitizen commit..."
    cz commit
    
    # Clean up
    rm -f "$COMMIT_TEMPLATE_FILE"
}

# Function to ask about pushing
ask_push() {
    echo
    read -p "Push changes to remote? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_status "Changes committed locally only"
        return
    fi
    
    # Check for remote
    local remote=$(git remote | head -1)
    if [ -z "$remote" ]; then
        print_warning "No remote repository configured"
        return
    fi
    
    local current_branch=$(git branch --show-current)
    print_status "Pushing to $remote/$current_branch..."
    
    if git push "$remote" "$current_branch"; then
        print_success "Changes pushed successfully!"
    else
        print_error "Failed to push changes"
        echo "You may need to pull first or resolve conflicts"
    fi
}

# Function to show usage
show_usage() {
    echo "thiLLMo Smart Commit Script"
    echo
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -q, --quick    Quick commit (skip file staging prompt)"
    echo "  -a, --all      Stage all changes automatically"
    echo "  -p, --push     Auto-push after commit"
    echo
    echo "This script will:"
    echo "  1. Check for changes and stage files"
    echo "  2. Analyze changes and suggest commit types"
    echo "  3. Run commitizen with AI prompt logging"
    echo "  4. Optionally push changes to remote"
}

# Main execution
main() {
    local quick_mode=false
    local auto_stage_all=false
    local auto_push=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -q|--quick)
                quick_mode=true
                shift
                ;;
            -a|--all)
                auto_stage_all=true
                shift
                ;;
            -p|--push)
                auto_push=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Pre-flight checks
    check_git_repo
    check_changes
    
    print_success "Starting thiLLMo Smart Commit..."
    echo
    
    # Show current state
    show_changes
    
    # Handle file staging
    if [ "$auto_stage_all" = true ]; then
        git add .
        print_success "All changes staged automatically"
    elif [ "$quick_mode" = false ]; then
        auto_stage
    fi
    
    # Commit with AI logging
    smart_commit
    
    # Handle pushing
    if [ "$auto_push" = true ]; then
        local remote=$(git remote | head -1)
        if [ -n "$remote" ]; then
            local current_branch=$(git branch --show-current)
            git push "$remote" "$current_branch"
            print_success "Changes pushed automatically!"
        fi
    else
        ask_push
    fi
    
    print_success "Smart commit completed!"
}

# Run main function with all arguments
main "$@"
