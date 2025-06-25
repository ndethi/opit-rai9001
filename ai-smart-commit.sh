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
    if echo "$diff_content" | grep -qE "^[+].*fix|^[+].*bug|^[+].*error|^[+].*issue|^[-].*bug|^[-].*error"; then
        has_bug_fixes=true
    fi
    
    # Detect new features/options
    if echo "$diff_content" | grep -qE "^[+].*--[a-z-]+|^[+].*-[a-z]|^[+].*new.*mode|^[+].*add.*option"; then
        has_new_features=true
    fi
    
    # Return analysis flags
    echo "$has_new_functions|$has_bug_fixes|$has_refactoring|$has_config_changes|$has_docs_updates|$has_new_features"
}

# Analyze diff content for specific insights
analyze_diff_insights() {
    local diff_output=$(git diff --cached)
    local insights=""
    
    # Function/method additions
    if echo "$diff_output" | grep -q "^+.*function \|^+.*def \|^+.*class \|^+.*interface"; then
        local new_funcs=$(echo "$diff_output" | grep -c "^+.*function \|^+.*def ")
        [ "$new_funcs" -gt 0 ] && insights+="$new_funcs new functions; "
    fi
    
    # Fast mode specific changes
    if echo "$diff_output" | grep -q "^+.*--fast"; then
        insights+="fast mode parameter support; "
    fi
    
    if echo "$diff_output" | grep -q "^+.*fast_mode.*=.*true"; then
        insights+="fast mode implementation; "
    fi
    
    # Interactive vs non-interactive changes
    if echo "$diff_output" | grep -q "^+.*interactive.*prompt\|^+.*read -p"; then
        insights+="interactive prompt handling; "
    fi
    
    # Commit message generation improvements
    if echo "$diff_output" | grep -q "^+.*generate.*commit.*message"; then
        insights+="enhanced commit message generation; "
    fi
    
    if echo "$diff_output" | grep -q "^+.*analyze.*diff\|^+.*diff.*content"; then
        insights+="improved diff analysis; "
    fi
    
    # Error handling and validation
    if echo "$diff_output" | grep -q "^+.*error.*handling\|^+.*validation\|^+.*check"; then
        insights+="better error handling; "
    fi
    
    if echo "$diff_output" | grep -q "^+.*\[\[ .*-gt\|^+.*integer.*expected"; then
        insights+="fixed bash syntax issues; "
    fi
    
    # Configuration and setup
    if echo "$diff_output" | grep -q "^+.*alias\|^+.*\.smart-commit"; then
        insights+="shell alias configuration; "
    fi
    
    if echo "$diff_output" | grep -q "^+.*setup\|^+.*install\|^+.*configure"; then
        insights+="setup automation; "
    fi
    
    # Documentation and README changes
    if echo "$diff_output" | grep -q "^+.*#.*Usage\|^+.*#.*Examples"; then
        insights+="usage documentation; "
    fi
    
    if echo "$diff_output" | grep -q "^+.*README\|^+.*\.md"; then
        insights+="documentation updates; "
    fi
    
    # Workflow and automation
    if echo "$diff_output" | grep -q "^+.*workflow\|^+.*\.github\|^+.*actions"; then
        insights+="GitHub Actions automation; "
    fi
    
    if echo "$diff_output" | grep -q "^+.*push.*origin\|^+.*git push"; then
        insights+="automated git push; "
    fi
    
    # Logging and tracking
    if echo "$diff_output" | grep -q "^+.*log.*commit\|^+.*commit.*history"; then
        insights+="commit tracking/logging; "
    fi
    
    if echo "$diff_output" | grep -q "^+.*AI.*context\|^+.*assistant"; then
        insights+="AI context logging; "
    fi
    
    # Script improvements
    if echo "$diff_output" | grep -q "^+.*case.*esac\|^+.*if.*then.*fi"; then
        insights+="control flow improvements; "
    fi
    
    # Remove trailing semicolon and space
    insights=$(echo "$insights" | sed 's/; $//')
    
    echo "$insights"
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
    
    # Get specific diff insights
    local diff_insights=$(analyze_diff_insights)
    
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
    
    # Generate highly specific subject based on actual changes and insights
    case "$commit_type" in
        "feat")
            if echo "$staged_files" | grep -q "ai-smart-commit\.sh"; then
                if echo "$diff_insights" | grep -q "fast mode parameter"; then
                    subject="add --fast mode for automated commits without interactive prompts"
                elif echo "$diff_insights" | grep -q "enhanced commit message generation"; then
                    subject="implement intelligent commit message generation with diff analysis"
                elif echo "$diff_insights" | grep -q "improved diff analysis"; then
                    subject="enhance diff analysis for more descriptive commit messages"
                elif echo "$diff_insights" | grep -q "AI context logging"; then
                    subject="add AI context and prompt logging functionality"
                elif echo "$diff_insights" | grep -q "automated git push"; then
                    subject="add automatic push capability for streamlined workflow"
                else
                    subject="expand smart commit system with new functionality"
                fi
            elif echo "$staged_files" | grep -q "\.github/workflows/"; then
                local workflow_files=$(echo "$staged_files" | grep "\.github/workflows/" | head -1)
                if echo "$workflow_files" | grep -q "latex"; then
                    subject="add automated LaTeX document building and validation"
                elif echo "$workflow_files" | grep -q "progress"; then
                    subject="implement weekly progress reporting automation"
                elif echo "$workflow_files" | grep -q "deadline"; then
                    subject="add automated deadline reminder system"
                else
                    subject="implement GitHub Actions CI/CD automation"
                fi
            elif echo "$staged_files" | grep -q "ontology" && echo "$diff_insights" | grep -q "new functions"; then
                subject="expand cultural ontology processing with new analysis functions"
            elif echo "$staged_files" | grep -q "og-rag" && echo "$diff_insights" | grep -q "new functions"; then
                subject="enhance OG-RAG system with advanced retrieval capabilities"
            elif echo "$diff_insights" | grep -q "shell alias configuration"; then
                subject="add shell aliases for improved development workflow efficiency"
            elif echo "$diff_insights" | grep -q "setup automation"; then
                subject="implement automated project setup and configuration system"
            else
                # Use file-based fallback with insights
                local primary_file=$(echo "$staged_files" | head -1 | sed 's|.*/||')
                subject="implement new functionality in $primary_file"
                [ -n "$diff_insights" ] && subject+=" ($diff_insights)"
            fi
            ;;
        "fix")
            if echo "$staged_files" | grep -q "ai-smart-commit\.sh"; then
                if echo "$diff_insights" | grep -q "fixed bash syntax"; then
                    subject="resolve bash integer comparison and syntax warnings"
                elif echo "$diff_insights" | grep -q "better error handling"; then
                    subject="improve error handling and validation in commit workflow"
                elif echo "$diff_insights" | grep -q "interactive prompt"; then
                    subject="fix interactive prompt handling and user input validation"
                else
                    subject="resolve script execution issues and improve reliability"
                fi
            elif echo "$diff_insights" | grep -q "error handling"; then
                subject="improve error handling and system validation"
            else
                local primary_file=$(echo "$staged_files" | head -1 | sed 's|.*/||')
                subject="resolve issues in $primary_file"
                [ -n "$diff_insights" ] && subject+=" (addressing: $diff_insights)"
            fi
            ;;
        "docs")
            if echo "$staged_files" | grep -q "SMART-COMMIT.*README"; then
                subject="add comprehensive smart commit system documentation and usage guide"
            elif echo "$staged_files" | grep -q "README.*\.md"; then
                if echo "$diff_insights" | grep -q "usage documentation"; then
                    subject="enhance README with detailed usage examples and configuration"
                else
                    subject="update main project documentation with current features"
                fi
            elif echo "$staged_files" | grep -q "docs/thesis/"; then
                subject="enhance thesis documentation structure and LaTeX formatting"
            elif echo "$diff_insights" | grep -q "documentation updates"; then
                local doc_count=$(echo "$staged_files" | grep -c "\.md$")
                subject="update $doc_count documentation files with improved content"
            else
                subject="improve project documentation and technical guides"
            fi
            ;;
        "chore")
            if echo "$staged_files" | grep -q "\.github/" && echo "$diff_insights" | grep -q "GitHub Actions"; then
                subject="update GitHub Actions workflow configuration and templates"
            elif echo "$staged_files" | grep -q "ISSUE_TEMPLATE"; then
                subject="add comprehensive GitHub issue templates for project management"
            elif echo "$diff_insights" | grep -q "shell alias configuration"; then
                subject="maintain shell aliases and command shortcuts for development"
            elif echo "$staged_files" | grep -qE "(package\.json|requirements|Pipfile)"; then
                subject="update project dependencies and package requirements"
            elif echo "$diff_insights" | grep -q "setup automation"; then
                subject="maintain project setup scripts and configuration automation"
            else
                local file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
                if [ "$file_count" -gt 5 ]; then
                    subject="reorganize project structure and maintain multiple configuration files"
                else
                    subject="update project configuration and maintenance files"
                fi
            fi
            ;;
        "test")
            subject="add comprehensive test coverage and validation for new features"
            ;;
        *)
            # Highly specific fallback using insights
            local primary_file=$(echo "$staged_files" | head -1 | sed 's|.*/||')
            if [ -n "$diff_insights" ]; then
                subject="update $primary_file with changes: $diff_insights"
            else
                subject="modify $primary_file with system improvements"
            fi
            ;;
    esac
    
    # Generate comprehensive body with detailed analysis
    local file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
    local new_files=$(git diff --cached --diff-filter=A --name-only | wc -l | tr -d ' ')
    local modified_files=$(git diff --cached --diff-filter=M --name-only | wc -l | tr -d ' ')
    local deleted_files=$(git diff --cached --diff-filter=D --name-only | wc -l | tr -d ' ')
    
    # Start building body
    body="Changes include $file_count files"
    
    # Add file type breakdown if multiple types
    local file_details=""
    [ "$new_files" -gt 0 ] && file_details+="$new_files new"
    [ "$modified_files" -gt 0 ] && [ -n "$file_details" ] && file_details+=", $modified_files modified"
    [ "$modified_files" -gt 0 ] && [ -z "$file_details" ] && file_details+="$modified_files modified"
    [ "$deleted_files" -gt 0 ] && [ -n "$file_details" ] && file_details+=", $deleted_files deleted"
    [ "$deleted_files" -gt 0 ] && [ -z "$file_details" ] && file_details+="$deleted_files deleted"
    
    [ -n "$file_details" ] && body+=": $file_details"
    
    # Add specific insights if available
    if [ -n "$diff_insights" ]; then
        body+=". Key improvements: $diff_insights"
    fi
    
    # Add file list if not too many files
    if [ "$file_count" -le 5 ]; then
        local file_list=$(echo "$staged_files" | sed 's|.*/||' | tr '\n' ', ' | sed 's/, $//')
        body+=". Files: $file_list"
    fi
    
    body+=". Auto-generated by thiLLMo smart commit system."
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
            --extra-verbose)
                verbose=true
                export VERBOSE_EXTRA=true
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
