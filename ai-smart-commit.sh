#!/bin/bash

# thiLLMo AI-Enhanced Smart Commit
# Advanced version with automatic AI context detection and prompt logging

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/.smart-commit-config"
HISTORY_FILE="$SCRIPT_DIR/.commit-history"
MAX_HISTORY=50

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Default AI settings
DEFAULT_ASSISTANT="GitHub Copilot"
DEFAULT_MODEL="GPT-4"

# Load configuration
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    else
        # Create default config
        cat > "$CONFIG_FILE" << EOF
# thiLLMo Smart Commit Configuration
DEFAULT_ASSISTANT="GitHub Copilot"
DEFAULT_MODEL="GPT-4"
AUTO_PUSH=false
QUICK_MODE=false
VERBOSE=true
SAVE_HISTORY=true
EOF
        echo -e "${GREEN}Created default configuration: $CONFIG_FILE${NC}"
    fi
}

# Save to history
save_to_history() {
    local commit_msg="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [ "$SAVE_HISTORY" = true ]; then
        echo "$timestamp|$commit_msg" >> "$HISTORY_FILE"
        
        # Keep only last MAX_HISTORY entries
        if [ -f "$HISTORY_FILE" ]; then
            tail -n "$MAX_HISTORY" "$HISTORY_FILE" > "$HISTORY_FILE.tmp"
            mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
        fi
    fi
}

# Enhanced file analysis
analyze_changes() {
    local changes_summary=""
    local staged_files=$(git diff --cached --name-only)
    
    # Count files properly
    if [ -z "$staged_files" ]; then
        echo "Analysis: 0 files"
        echo "chore"
        return
    fi
    
    local file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
    
    # Categorize changes (handle empty results properly)
    local new_files_list=$(git diff --cached --diff-filter=A --name-only)
    local modified_files_list=$(git diff --cached --diff-filter=M --name-only)
    local deleted_files_list=$(git diff --cached --diff-filter=D --name-only)
    
    local new_files=0
    local modified_files=0
    local deleted_files=0
    
    [ -n "$new_files_list" ] && new_files=$(echo "$new_files_list" | wc -l | tr -d ' ')
    [ -n "$modified_files_list" ] && modified_files=$(echo "$modified_files_list" | wc -l | tr -d ' ')
    [ -n "$deleted_files_list" ] && deleted_files=$(echo "$deleted_files_list" | wc -l | tr -d ' ')
    
    # Analyze file types (handle empty results properly)
    local docs_changed=0
    local code_changed=0
    local config_changed=0
    local test_changed=0
    
    local docs_files=$(echo "$staged_files" | grep -E "\.(md|txt|rst|tex)$" || true)
    local code_files=$(echo "$staged_files" | grep -E "\.(py|js|ts|java|cpp|c|go|rs|php)$" || true)
    local config_files=$(echo "$staged_files" | grep -E "\.(json|yaml|yml|toml|cfg|ini)$" || true)
    local test_files=$(echo "$staged_files" | grep -E "(test|spec)" || true)
    
    [ -n "$docs_files" ] && docs_changed=$(echo "$docs_files" | wc -l | tr -d ' ')
    [ -n "$code_files" ] && code_changed=$(echo "$code_files" | wc -l | tr -d ' ')
    [ -n "$config_files" ] && config_changed=$(echo "$config_files" | wc -l | tr -d ' ')
    [ -n "$test_files" ] && test_changed=$(echo "$test_files" | wc -l | tr -d ' ')
    
    # Generate analysis
    changes_summary="Analysis: $file_count files"
    [ "$new_files" -gt 0 ] && changes_summary+=", $new_files new"
    [ "$modified_files" -gt 0 ] && changes_summary+=", $modified_files modified"
    [ "$deleted_files" -gt 0 ] && changes_summary+=", $deleted_files deleted"
    
    echo "$changes_summary"
    
    # Suggest commit type based on analysis
    if [ "$new_files" -gt "$modified_files" ] && [ "$code_changed" -gt 0 ]; then
        echo "feat"
    elif [ "$docs_changed" -gt 0 ] && [ "$code_changed" -eq 0 ]; then
        echo "docs"
    elif [ "$test_changed" -gt 0 ]; then
        echo "test"
    elif [ "$config_changed" -gt 0 ] && [ "$code_changed" -eq 0 ]; then
        echo "chore"
    elif [ "$modified_files" -gt "$new_files" ]; then
        echo "fix"
    else
        echo "feat"
    fi
}

# Generate intelligent commit suggestions
generate_smart_suggestions() {
    local commit_type="$1"
    local staged_files=$(git diff --cached --name-only)
    local suggestions=()
    
    # Context-aware suggestions based on file patterns
    case "$commit_type" in
        "feat")
            if echo "$staged_files" | grep -q "src/"; then
                suggestions+=("feat: implement new core functionality")
                suggestions+=("feat: add new system component")
            fi
            if echo "$staged_files" | grep -q "\.github/"; then
                suggestions+=("feat: add GitHub automation workflows")
                suggestions+=("feat: implement CI/CD pipeline")
            fi
            ;;
        "docs")
            if echo "$staged_files" | grep -q "README"; then
                suggestions+=("docs: update project README")
                suggestions+=("docs: improve getting started guide")
            fi
            if echo "$staged_files" | grep -q "docs/"; then
                suggestions+=("docs: enhance documentation structure")
                suggestions+=("docs: add technical specifications")
            fi
            ;;
        "chore")
            if echo "$staged_files" | grep -qE "(package\.json|requirements|Pipfile)"; then
                suggestions+=("chore: update project dependencies")
            fi
            if echo "$staged_files" | grep -q "\.github/"; then
                suggestions+=("chore: update GitHub configuration")
            fi
            ;;
    esac
    
    # Project-specific suggestions for thiLLMo
    if echo "$staged_files" | grep -q "ontology"; then
        suggestions+=("feat: enhance cultural ontology structure")
        suggestions+=("feat: add new ontology components")
    fi
    
    if echo "$staged_files" | grep -q "og-rag"; then
        suggestions+=("feat: improve OG-RAG system implementation")
        suggestions+=("fix: resolve OG-RAG pipeline issues")
    fi
    
    if echo "$staged_files" | grep -q "proverb"; then
        suggestions+=("feat: add Kikuyu proverb processing")
        suggestions+=("docs: document proverb translation methodology")
    fi
    
    # Print suggestions
    if [ ${#suggestions[@]} -gt 0 ]; then
        echo -e "${CYAN}💡 Smart suggestions:${NC}"
        for i in "${!suggestions[@]}"; do
            echo "   $((i+1)). ${suggestions[$i]}"
        done
        echo
    fi
}

# Detect recent AI interactions (placeholder for future enhancement)
detect_ai_context() {
    # This could be enhanced to detect:
    # - Recent clipboard content with prompts
    # - VS Code extension activity
    # - Browser history for AI tools
    # - Terminal history for AI commands
    
    local context=""
    local assistant="$DEFAULT_ASSISTANT"
    local model="$DEFAULT_MODEL"
    
    # Simple heuristic: check recent command history
    if command -v history &> /dev/null; then
        local recent_history=$(history 10)
        if echo "$recent_history" | grep -q "copilot\|chatgpt\|claude"; then
            context="Recent AI tool usage detected"
        fi
    fi
    
    echo "$context|$assistant|$model"
}

# Analyze specific changes in detail
analyze_file_changes() {
    local staged_files=$(git diff --cached --name-only)
    local changes_details=""
    
    # Analyze specific file changes for better commit messages
    local has_new_functions=false
    local has_bug_fixes=false
    local has_refactoring=false
    local has_config_changes=false
    local has_docs_updates=false
    local has_new_features=false
    
    # Check for specific patterns in diff
    local diff_content=$(git diff --cached)
    
    # Detect new function/method additions
    if echo "$diff_content" | grep -q "^+.*function\|^+.*def \|^+.*const \|^+.*let \|^+.*var \|^+.*class "; then
        has_new_functions=true
    fi
    
    # Detect bug fix patterns
    if echo "$diff_content" | grep -qE "^+.*fix|^+.*bug|^+.*error|^+.*issue|^-.*bug|^-.*error"; then
        has_bug_fixes=true
    fi
    
    # Detect new features/options
    if echo "$diff_content" | grep -qE "^+.*--[a-z-]+|^+.*-[a-z]|^+.*new.*mode|^+.*add.*option"; then
        has_new_features=true
    fi
    
    # Return analysis flags
    echo "$has_new_functions|$has_bug_fixes|$has_refactoring|$has_config_changes|$has_docs_updates|$has_new_features"
}

# Generate smart commit message with detailed analysis
generate_smart_commit_message() {
    local commit_type="$1"
    local staged_files=$(git diff --cached --name-only)
    local scope=""
    local subject=""
    local body=""
    
    # Get detailed change analysis
    local change_analysis=$(analyze_file_changes)
    IFS='|' read -r has_new_functions has_bug_fixes has_refactoring has_config_changes has_docs_updates has_new_features <<< "$change_analysis"
    
    # Determine scope based on file patterns (more specific)
    if echo "$staged_files" | grep -q "ai-smart-commit\.sh"; then
        scope="smart-commit"
    elif echo "$staged_files" | grep -q "smart-commit\.sh"; then
        scope="commit-tools"
    elif echo "$staged_files" | grep -q "setup-.*\.sh"; then
        scope="setup"
    elif echo "$staged_files" | grep -q "src/ontology/"; then
        scope="ontology"
    elif echo "$staged_files" | grep -q "src/og-rag/"; then
        scope="og-rag"
    elif echo "$staged_files" | grep -q "docs/thesis/"; then
        scope="thesis"
    elif echo "$staged_files" | grep -q "\.github/workflows/"; then
        scope="ci"
    elif echo "$staged_files" | grep -q "\.github/"; then
        scope="github"
    elif echo "$staged_files" | grep -q "admin/"; then
        scope="admin"
    elif echo "$staged_files" | grep -q "data/"; then
        scope="data"
    elif echo "$staged_files" | grep -q "src/"; then
        scope="core"
    fi
    
    # Generate detailed subject based on actual changes
    case "$commit_type" in
        "feat")
            if echo "$staged_files" | grep -q "ai-smart-commit\.sh" && [ "$has_new_features" = true ]; then
                # Analyze what new features were added
                local diff_content=$(git diff --cached)
                if echo "$diff_content" | grep -q "\--fast"; then
                    subject="add fast mode for automated commits without interactive prompts"
                elif echo "$diff_content" | grep -q "\--quick"; then
                    subject="add quick mode for streamlined commit workflow"
                elif echo "$diff_content" | grep -q "generate_smart_commit_message"; then
                    subject="add intelligent commit message generation"
                else
                    subject="add new command-line options and functionality"
                fi
            elif echo "$staged_files" | grep -q "\.github/workflows/"; then
                local workflow_files=$(echo "$staged_files" | grep "\.github/workflows/" | head -3)
                if echo "$workflow_files" | grep -q "latex"; then
                    subject="add LaTeX document build automation"
                elif echo "$workflow_files" | grep -q "progress"; then
                    subject="add weekly progress reporting workflow"
                else
                    subject="add GitHub automation workflows"
                fi
            elif echo "$staged_files" | grep -q "ontology"; then
                subject="enhance cultural ontology structure and processing"
            elif echo "$staged_files" | grep -q "og-rag"; then
                subject="improve OG-RAG system implementation"
            elif [ "$has_new_functions" = true ]; then
                subject="add new functions and core functionality"
            else
                # Fallback: try to infer from file names and content
                local primary_file=$(echo "$staged_files" | head -1)
                if echo "$primary_file" | grep -q "README"; then
                    subject="add comprehensive project documentation"
                elif echo "$primary_file" | grep -q "setup"; then
                    subject="add project setup and configuration tools"
                else
                    subject="implement new features and functionality"
                fi
            fi
            ;;
        "fix")
            if echo "$staged_files" | grep -q "ai-smart-commit\.sh" && [ "$has_bug_fixes" = true ]; then
                local diff_content=$(git diff --cached)
                if echo "$diff_content" | grep -q "integer.*expected"; then
                    subject="resolve bash integer comparison warnings in file analysis"
                elif echo "$diff_content" | grep -q "wc -l"; then
                    subject="fix file counting logic and error handling"
                else
                    subject="resolve script execution issues and improve error handling"
                fi
            elif echo "$staged_files" | grep -q "ontology"; then
                subject="resolve ontology processing and validation issues"
            elif echo "$staged_files" | grep -q "og-rag"; then
                subject="fix OG-RAG pipeline bugs and data processing"
            else
                # Try to infer from diff content
                local diff_content=$(git diff --cached)
                if echo "$diff_content" | grep -qE "^-.*error|^-.*bug"; then
                    subject="resolve identified bugs and error conditions"
                else
                    subject="fix system issues and improve reliability"
                fi
            fi
            ;;
        "docs")
            if echo "$staged_files" | grep -q "README.*\.md"; then
                if echo "$staged_files" | grep -q "SMART-COMMIT"; then
                    subject="add comprehensive smart commit system documentation"
                else
                    subject="update main project documentation and usage guides"
                fi
            elif echo "$staged_files" | grep -q "docs/thesis/"; then
                subject="enhance thesis documentation and LaTeX structure"
            elif echo "$staged_files" | grep -q "\.md$"; then
                local doc_count=$(echo "$staged_files" | grep -c "\.md$")
                if [ "$doc_count" -gt 3 ]; then
                    subject="add comprehensive project documentation structure"
                else
                    subject="update documentation and user guides"
                fi
            else
                subject="improve project documentation and comments"
            fi
            ;;
        "chore")
            if echo "$staged_files" | grep -q "\.github/"; then
                if echo "$staged_files" | grep -q "ISSUE_TEMPLATE"; then
                    subject="add GitHub issue templates for project management"
                else
                    subject="update GitHub configuration and automation"
                fi
            elif echo "$staged_files" | grep -qE "(package\.json|requirements|Pipfile)"; then
                subject="update project dependencies and package configuration"
            elif echo "$staged_files" | grep -q "alias"; then
                subject="add shell aliases for improved development workflow"
            elif echo "$staged_files" | grep -q "config"; then
                subject="update configuration files and project settings"
            else
                local file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
                if [ "$file_count" -gt 10 ]; then
                    subject="restructure project organization and maintenance files"
                else
                    subject="update project configuration and maintenance files"
                fi
            fi
            ;;
        "test")
            subject="add/update test coverage and validation"
            ;;
        *)
            # Analyze the most changed file for hints
            local primary_file=$(echo "$staged_files" | head -1)
            subject="update $(basename "$primary_file") and related components"
            ;;
    esac
    
    # Generate detailed body with specific changes
    local file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
    local new_files=$(git diff --cached --diff-filter=A --name-only | wc -l | tr -d ' ')
    local modified_files=$(git diff --cached --diff-filter=M --name-only | wc -l | tr -d ' ')
    local deleted_files=$(git diff --cached --diff-filter=D --name-only | wc -l | tr -d ' ')
    
    # Create detailed body
    body="Changes include"
    if [ "$new_files" -gt 0 ] && [ "$modified_files" -gt 0 ]; then
        body+=": $new_files new files and $modified_files modifications"
    elif [ "$new_files" -gt 0 ]; then
        body+=": $new_files new files"
    elif [ "$modified_files" -gt 0 ]; then
        body+=": $modified_files file modifications"
    else
        body+=": $file_count file updates"
    fi
    
    [ "$deleted_files" -gt 0 ] && body+=", $deleted_files deletions"
    
    # Add specific change details
    if [ "$has_new_functions" = true ]; then
        body+=". Adds new functions and methods"
    fi
    if [ "$has_new_features" = true ]; then
        body+=". Introduces new features and command-line options"
    fi
    if [ "$has_bug_fixes" = true ]; then
        body+=". Resolves bugs and error conditions"
    fi
    
    body+=". Auto-generated by thiLLMo smart commit system."
    
    # Format final commit message
    local commit_msg="$commit_type"
    [ -n "$scope" ] && commit_msg+="($scope)"
    commit_msg+=": $subject"
    
    echo "$commit_msg|$body"
}

# Fast commit without interactive prompts
fast_commit() {
    local suggested_type="$1"
    local analysis="$2"
    
    echo -e "${PURPLE}⚡ Fast commit mode - generating automated commit...${NC}"
    echo
    
    # Show brief analysis
    echo -e "${BLUE}📊 Analysis:${NC} $analysis"
    echo -e "${BLUE}📁 Suggested type:${NC} $suggested_type"
    echo
    
    # Generate smart commit message
    local commit_data=$(generate_smart_commit_message "$suggested_type")
    IFS='|' read -r commit_msg commit_body <<< "$commit_data"
    
    # Detect AI context
    local ai_context=$(detect_ai_context)
    IFS='|' read -r context assistant model <<< "$ai_context"
    
    # Build full commit message with AI context
    local full_commit_msg="$commit_msg

$commit_body"
    
    # Add AI context if available
    if [ -n "$context" ] || [ -n "$assistant" ] || [ -n "$model" ]; then
        full_commit_msg+="

"
        [ -n "$context" ] && full_commit_msg+="Prompt-context: $context
"
        [ -n "$assistant" ] && full_commit_msg+="AI-assistant: $assistant
"
        [ -n "$model" ] && full_commit_msg+="AI-model: $model"
    fi
    
    echo -e "${GREEN}📝 Generated commit message:${NC}"
    echo -e "${CYAN}$commit_msg${NC}"
    echo
    
    # Create commit directly
    if git commit -m "$full_commit_msg"; then
        # Save successful commit to history
        save_to_history "$commit_msg"
        echo -e "${GREEN}✅ Fast commit created successfully!${NC}"
        return 0
    else
        echo -e "${RED}❌ Fast commit failed${NC}"
        return 1
    fi
}

# Enhanced commitizen wrapper
enhanced_commit() {
    local suggested_type="$1"
    local analysis="$2"
    local fast_mode="$3"
    
    if [ "$fast_mode" = true ]; then
        fast_commit "$suggested_type" "$analysis"
        return $?
    fi
    
    echo -e "${PURPLE}🤖 Starting AI-enhanced commit process...${NC}"
    echo
    
    # Show detailed analysis
    echo -e "${BLUE}📊 Change Analysis:${NC}"
    echo "   $analysis"
    echo
    
    # Show file statistics
    echo -e "${BLUE}📁 File Changes:${NC}"
    git diff --cached --stat
    echo
    
    # Generate and show suggestions
    generate_smart_suggestions "$suggested_type"
    
    # Detect AI context
    local ai_context=$(detect_ai_context)
    IFS='|' read -r context assistant model <<< "$ai_context"
    
    # Pre-fill some values for commitizen
    export CZ_PRE_COMMIT_TYPE="$suggested_type"
    export CZ_PRE_ASSISTANT="$assistant"
    export CZ_PRE_MODEL="$model"
    export CZ_PRE_CONTEXT="$context"
    
    echo -e "${GREEN}🚀 Launching commitizen with AI context...${NC}"
    echo
    
    # Run commitizen
    if cz commit; then
        # Save successful commit to history
        local commit_msg=$(git log -1 --pretty=format:"%s")
        save_to_history "$commit_msg"
        echo -e "${GREEN}✅ Commit created successfully!${NC}"
        return 0
    else
        echo -e "${RED}❌ Commit cancelled or failed${NC}"
        return 1
    fi
}

# Smart push with branch detection
smart_push() {
    local auto_push="$1"
    
    if [ "$auto_push" = true ]; then
        echo -e "${BLUE}🔄 Auto-pushing changes...${NC}"
    else
        echo
        echo -e "${YELLOW}📤 Push changes to remote?${NC}"
        echo "   Current branch: $(git branch --show-current)"
        echo "   Remote: $(git remote | head -1 || echo 'none')"
        echo
        read -p "Push now? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            echo -e "${BLUE}📝 Changes committed locally only${NC}"
            return 0
        fi
    fi
    
    local remote=$(git remote | head -1)
    if [ -z "$remote" ]; then
        echo -e "${YELLOW}⚠️  No remote repository configured${NC}"
        return 1
    fi
    
    local current_branch=$(git branch --show-current)
    echo -e "${BLUE}🚀 Pushing to $remote/$current_branch...${NC}"
    
    if git push "$remote" "$current_branch"; then
        echo -e "${GREEN}✅ Changes pushed successfully!${NC}"
        
        # Show remote URL if available
        local remote_url=$(git remote get-url "$remote" 2>/dev/null || echo "")
        if [ -n "$remote_url" ]; then
            echo -e "${CYAN}🔗 Remote URL: $remote_url${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Failed to push changes${NC}"
        echo -e "${YELLOW}💡 You may need to pull first or resolve conflicts${NC}"
        return 1
    fi
}

# Show enhanced usage
show_usage() {
    cat << EOF
${PURPLE}thiLLMo AI-Enhanced Smart Commit Script${NC}

${CYAN}Usage:${NC} $0 [options] [message]

${CYAN}Options:${NC}
  -h, --help       Show this help message
  -q, --quick      Quick mode (auto-stage all, skip prompts)
  -f, --fast       Fast mode (auto-generate commit, no interaction)
  -a, --all        Stage all changes automatically
  -p, --push       Auto-push after successful commit
  -v, --verbose    Verbose output (default)
  -s, --silent     Minimal output
  -c, --config     Show current configuration
  --history        Show recent commit history

${CYAN}Features:${NC}
  🤖 AI-powered commit message suggestions
  📊 Intelligent change analysis
  🔍 Automatic commit type detection
  📝 AI prompt and context logging
  🚀 Smart push with branch detection
  📚 Commit history tracking
  ⚙️  Configurable defaults

${CYAN}Examples:${NC}
  $0                    # Interactive mode with full analysis
  $0 -qa               # Quick commit all changes
  $0 -qap              # Quick commit all changes and push
  $0 -f                # Fast auto-generated commit
  $0 -fap              # Fast commit, stage all, and push
  $0 --config          # Show current configuration

${CYAN}Mode Comparison:${NC}
  ${GREEN}Interactive${NC}  - Full commitizen prompt with suggestions
  ${YELLOW}Quick${NC}        - Auto-stage files, but still interactive commit
  ${PURPLE}Fast${NC}         - Fully automated commit with smart defaults

${CYAN}AI Context Logging:${NC}
This script integrates with your existing commitizen configuration
to automatically log AI assistant interactions, prompts, and context
for better development tracking and reproducibility.

EOF
}

# Show configuration
show_config() {
    echo -e "${PURPLE}Current Configuration:${NC}"
    echo
    if [ -f "$CONFIG_FILE" ]; then
        cat "$CONFIG_FILE"
    else
        echo "No configuration file found"
    fi
    echo
    echo -e "${CYAN}Config file location: $CONFIG_FILE${NC}"
}

# Show commit history
show_history() {
    echo -e "${PURPLE}Recent Commit History:${NC}"
    echo
    if [ -f "$HISTORY_FILE" ]; then
        tail -n 10 "$HISTORY_FILE" | while IFS='|' read -r timestamp message; do
            echo -e "${CYAN}$timestamp${NC} - $message"
        done
    else
        echo "No commit history found"
    fi
}

# Main function
main() {
    local quick_mode=false
    local fast_mode=false
    local auto_stage_all=false
    local auto_push=false
    local verbose=true
    local commit_message=""
    
    # Load configuration
    load_config
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -q|--quick)
                quick_mode=true
                auto_stage_all=true
                shift
                ;;
            -f|--fast)
                fast_mode=true
                auto_stage_all=true
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
            -v|--verbose)
                verbose=true
                shift
                ;;
            -s|--silent)
                verbose=false
                shift
                ;;
            -c|--config)
                show_config
                exit 0
                ;;
            --history)
                show_history
                exit 0
                ;;
            -*)
                echo -e "${RED}Unknown option: $1${NC}"
                show_usage
                exit 1
                ;;
            *)
                commit_message="$1"
                shift
                ;;
        esac
    done
    
    # Check git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}❌ Not in a git repository!${NC}"
        exit 1
    fi
    
    # Check for changes
    if git diff --quiet && git diff --cached --quiet; then
        echo -e "${YELLOW}⚠️  No changes detected${NC}"
        if [ "$quick_mode" = false ] && [ "$fast_mode" = false ]; then
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo -e "${BLUE}👋 Goodbye!${NC}"
                exit 0
            fi
        else
            echo -e "${BLUE}👋 Nothing to commit${NC}"
            exit 0
        fi
    fi
    
    # Show mode indicator
    if [ "$fast_mode" = true ]; then
        echo -e "${PURPLE}⚡ thiLLMo Fast Commit Mode${NC}"
    else
        echo -e "${GREEN}🎯 thiLLMo AI-Enhanced Smart Commit${NC}"
    fi
    echo
    
    # Auto-stage if requested
    if [ "$auto_stage_all" = true ]; then
        git add .
        if [ "$fast_mode" = true ]; then
            echo -e "${GREEN}📁 All changes staged for fast commit${NC}"
        else
            echo -e "${GREEN}📁 All changes staged automatically${NC}"
        fi
    else
        # Show current status and ask about staging
        echo -e "${BLUE}📋 Current repository status:${NC}"
        git status --short
        echo
        
        if [ "$(git diff --cached --name-only | wc -l)" -eq 0 ]; then
            read -p "Stage all changes? (Y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                git add .
                echo -e "${GREEN}📁 All changes staged${NC}"
            fi
        fi
    fi
    
    # Analyze changes
    if [ "$fast_mode" = true ]; then
        echo -e "${BLUE}⚡ Fast analysis...${NC}"
    else
        echo -e "${BLUE}🔍 Analyzing changes...${NC}"
    fi
    
    local analysis_result=$(analyze_changes)
    local suggested_type=$(echo "$analysis_result" | tail -1)
    local analysis_summary=$(echo "$analysis_result" | head -1)
    
    # Enhanced commit process
    if enhanced_commit "$suggested_type" "$analysis_summary" "$fast_mode"; then
        # Handle push
        smart_push "$auto_push"
        echo
        if [ "$fast_mode" = true ]; then
            echo -e "${GREEN}⚡ Fast commit completed successfully!${NC}"
        else
            echo -e "${GREEN}🎉 Smart commit completed successfully!${NC}"
        fi
    else
        echo -e "${RED}💥 Commit process failed${NC}"
        exit 1
    fi
}

# Run main function
main "$@"
