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

# Enhanced AI context detection and prompt inference
detect_ai_context() {
    local context=""
    local assistant="$DEFAULT_ASSISTANT"
    local model="$DEFAULT_MODEL"
    local prompt=""
    
    # Check VS Code environment for Copilot
    if command -v code &> /dev/null && pgrep -f "code" > /dev/null; then
        if [ -d "$HOME/.vscode/extensions" ] && ls "$HOME/.vscode/extensions" | grep -q copilot; then
            assistant="GitHub Copilot"
            model="GPT-4"
            context="VS Code with Copilot active"
        fi
    fi
    
    # Check recent shell command history for AI tool usage
    if command -v history &> /dev/null; then
        local recent_history=$(history 20 2>/dev/null || true)
        if echo "$recent_history" | grep -q "copilot\|github.*copilot"; then
            assistant="GitHub Copilot"
            context="Recent Copilot CLI usage detected"
        elif echo "$recent_history" | grep -q "chatgpt\|openai"; then
            assistant="ChatGPT"
            model="GPT-4"
            context="Recent OpenAI tool usage"
        elif echo "$recent_history" | grep -q "claude\|anthropic"; then
            assistant="Claude"
            model="Claude-3"
            context="Recent Anthropic tool usage"
        fi
    fi
    
    # Infer prompt from commit changes and context with enhanced specificity
    local staged_files=$(git diff --cached --name-only)
    if echo "$staged_files" | grep -q "ai-smart-commit\.sh"; then
        local diff_content=$(git diff --cached --no-color)
        if echo "$diff_content" | grep -q "automatic.*staging\|git add"; then
            prompt="Modify the AI smart commit script to automatically stage all changes without user intervention, eliminating the need to run git add manually"
            context="Script automation enhancement - automatic staging implementation"
        elif echo "$diff_content" | grep -q "fast.*mode.*push\|auto.*push"; then
            prompt="Test the combination of fast mode and auto-push flags to achieve complete automation in the commit workflow"
            context="Testing automated commit workflow with combined flags"
        elif echo "$diff_content" | grep -q "commit.*message.*generation\|specific.*commit\|doc_content_context\|extract_content_context"; then
            prompt="Re-engineer the commit message generator to be more specific about file content and context rather than generic patterns, and incorporate prompt context for better commit messages"
            context="Enhancing commit message specificity by analyzing actual content changes and incorporating user prompts"
        elif echo "$diff_content" | grep -q "contextualize.*commit.*message\|pull.*prompt"; then
            prompt="Further contextualize commit messages by incorporating the actual prompt that resulted in the change"
            context="Adding prompt-driven context to commit message generation for better traceability"
        fi
    elif echo "$staged_files" | grep -q "README.*chapters\|docs.*thesis"; then
        local diff_content=$(git diff --cached --no-color)
        if echo "$diff_content" | grep -q "naming.*convention\|OPIT.*STUDENT.*AUTHOR"; then
            prompt="Create a semantic naming convention for thesis documentation files that includes institution, student ID, author, document type, and version information"
            context="Establishing systematic thesis document naming and organization standards"
        elif echo "$diff_content" | grep -q "template.*reference\|\.\.\/template"; then
            prompt="Add reference to OPIT LaTeX template location in thesis documentation structure"
            context="Integrating institutional template requirements into thesis workflow"
        elif echo "$diff_content" | grep -q "remove.*test.*text\|clean.*up.*test"; then
            prompt="Remove test text from README file to clean up documentation"
            context="Documentation cleanup and maintenance"
        fi
    elif echo "$staged_files" | grep -q "README"; then
        local diff_content=$(git diff --cached --no-color)
        if echo "$diff_content" | grep -q "test.*comment"; then
            prompt="Add test comments to README to verify the enhanced AI smart commit functionality"
            context="Testing documentation updates for script validation"
        fi
    fi
    
    # Default prompt based on commit type if none detected
    if [ -z "$prompt" ]; then
        local commit_type=$(analyze_changes | tail -1)
        case "$commit_type" in
            "feat") prompt="Implement new feature or functionality" ;;
            "fix") prompt="Fix bugs or resolve issues" ;;
            "docs") prompt="Update documentation" ;;
            "chore") prompt="Perform maintenance tasks" ;;
            *) prompt="Make necessary code changes" ;;
        esac
    fi
    
    echo "$prompt|$context|$assistant|$model"
}

# Analyze specific changes in detail for better commit messages
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
    local has_automation_changes=false
    local has_testing_changes=false
    
    # Check for specific patterns in diff
    local diff_content=$(git diff --cached --no-color)
    
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
    
    # Detect automation improvements
    if echo "$diff_content" | grep -qE "^[+].*auto|^[+].*automatic|^[-].*manual|^[+].*streamline"; then
        has_automation_changes=true
    fi
    
    # Detect testing additions
    if echo "$diff_content" | grep -qE "^[+].*test|^[+].*# Test|^[+].*testing"; then
        has_testing_changes=true
    fi
    
    # Return analysis flags
    echo "$has_new_functions|$has_bug_fixes|$has_refactoring|$has_config_changes|$has_docs_updates|$has_new_features|$has_automation_changes|$has_testing_changes"
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

# Extract specific content context from diff to make commit messages more precise
extract_content_context() {
    local diff_content=$(git diff --cached --no-color)
    local staged_files=$(git diff --cached --name-only)
    local content_context=""
    
    # Get AI context for prompt-driven context detection
    local ai_context_for_analysis=$(detect_ai_context)
    local ai_prompt=$(echo "$ai_context_for_analysis" | cut -d'|' -f1)
    
    # Prioritize the actual file being changed over content patterns
    # This prevents false positives where we're editing a file that contains certain keywords
    
    # First check what files are being modified - this is more reliable than content patterns
    if echo "$staged_files" | grep -q "ai-smart-commit\.sh"; then
        # We're modifying the smart commit script itself
        if [ -n "$ai_prompt" ] && echo "$ai_prompt" | grep -q "contextualize.*commit.*message\|pull.*prompt"; then
            content_context="prompt-driven commit message contextualization"
        elif echo "$diff_content" | grep -q "^+.*technical_changes.*=\|^-.*technical_changes.*="; then
            content_context="commit message generation logic improvements"
        elif echo "$diff_content" | grep -q "^+.*extract_content_context\|^-.*extract_content_context"; then
            content_context="content context detection refinements"
        elif echo "$diff_content" | grep -q "^+.*generate_smart_commit_message\|^-.*generate_smart_commit_message"; then
            content_context="smart commit message algorithm enhancements"
        elif echo "$diff_content" | grep -q "^+.*fast_mode\|^+.*--fast"; then
            content_context="automated workflow features"
        else
            content_context="smart commit functionality improvements"
        fi
    elif echo "$staged_files" | grep -q "docs/thesis/chapters/README\.md"; then
        # We're modifying thesis documentation
        if [ -n "$ai_prompt" ] && echo "$ai_prompt" | grep -q "remove.*test.*text\|clean.*up"; then
            content_context="documentation cleanup and maintenance"
        elif echo "$diff_content" | grep -q "^+.*OPIT.*STUDENT_ID.*AUTHOR_LASTNAME"; then
            content_context="thesis document naming convention guidelines"
        elif echo "$diff_content" | grep -q "^+.*template.*reference\|^+.*\.\.\/template"; then
            content_context="LaTeX template integration guidelines"
        elif echo "$diff_content" | grep -q "^+.*Chapter.*Structure\|^+.*Writing.*Guidelines"; then
            content_context="thesis organization and structure documentation"
        else
            content_context="thesis documentation updates"
        fi
    elif echo "$staged_files" | grep -q "src/ontology/"; then
        content_context="cultural ontology framework development"
    elif echo "$staged_files" | grep -q "src/og-rag/"; then
        content_context="ontology-grounded RAG system implementation"
    elif echo "$staged_files" | grep -q "data/proverbs/"; then
        content_context="cultural proverb data and processing"
    elif echo "$staged_files" | grep -q "src/evaluation/"; then
        content_context="research evaluation methodology"
    elif echo "$staged_files" | grep -q "docs/proposal/"; then
        content_context="research proposal documentation"
    elif echo "$staged_files" | grep -q "admin/"; then
        content_context="project administration and management"
    # Only use content patterns as fallback for generic files
    elif echo "$diff_content" | grep -q "^+.*cultural.*ontology\|^+.*kikuyu.*proverb"; then
        content_context="cultural knowledge representation framework"
    elif echo "$diff_content" | grep -q "^+.*evaluation.*methodology\|^+.*experimental.*design"; then
        content_context="research methodology framework"
    fi
    
    echo "$content_context"
}

# Generate highly specific commit messages based on deep diff analysis
generate_smart_commit_message() {
    local commit_type="$1"
    local staged_files=$(git diff --cached --name-only)
    local diff_content=$(git diff --cached --no-color)
    local scope=""
    local subject=""
    local body=""
    
    # Extract specific content context for more precise messaging
    local content_context=$(extract_content_context)
    
    # Enhanced scope detection with priority-based file matching
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
    elif echo "$staged_files" | grep -q "src/evaluation/"; then
        scope="evaluation"
    elif echo "$staged_files" | grep -q "docs/thesis/"; then
        scope="thesis"
    elif echo "$staged_files" | grep -q "\.github/workflows/"; then
        scope="ci"
    elif echo "$staged_files" | grep -q "\.github/"; then
        scope="github"
    elif echo "$staged_files" | grep -q "admin/"; then
        scope="admin"
    elif echo "$staged_files" | grep -q "data/proverbs/"; then
        scope="proverbs"
    elif echo "$staged_files" | grep -q "data/"; then
        scope="data"
    elif echo "$staged_files" | grep -q "src/"; then
        scope="core"
    elif echo "$staged_files" | grep -q "docs/"; then
        scope="docs"
    elif echo "$staged_files" | grep -q "presentations/"; then
        scope="presentations"
    fi
    
    # Deep diff analysis - extract specific code changes
    local added_functions=$(echo "$diff_content" | grep -c "^+.*function \|^+.*def \|^+.*const [a-zA-Z_][a-zA-Z0-9_]* = \|^+.*let [a-zA-Z_][a-zA-Z0-9_]* = ")
    local added_methods=$(echo "$diff_content" | grep -c "^+.*[a-zA-Z_][a-zA-Z0-9_]*([^)]*) {")
    local added_classes=$(echo "$diff_content" | grep -c "^+.*class [A-Z][a-zA-Z0-9_]*")
    local added_parameters=$(echo "$diff_content" | grep -c "^+.*--[a-z-][a-z-]*\|^+.*-[a-z]")
    local fixed_errors=$(echo "$diff_content" | grep -c "^-.*error\|^-.*bug\|^+.*fix\|^+.*resolve")
    local added_tests=$(echo "$diff_content" | grep -c "^+.*test\|^+.*describe\|^+.*it(")
    local config_changes=$(echo "$diff_content" | grep -c "^+.*config\|^+.*\.json\|^+.*\.yaml\|^+.*\.yml")
    
    # Extract specific function/variable names from additions
    local new_function_names=$(echo "$diff_content" | grep "^+.*function \|^+.*def \|^+.*const [a-zA-Z_]" | sed -E 's/^[+].*[[:space:]](function[[:space:]]+|def[[:space:]]+|const[[:space:]]+|let[[:space:]]+)([a-zA-Z_][a-zA-Z0-9_]*).*/\2/' | head -3 | tr '\n' ', ' | sed 's/, $//')
    
    # Extract new command-line options
    local new_options=$(echo "$diff_content" | grep "^+.*--[a-z-]" | sed -E 's/.*(-[-a-z]+).*/\1/' | head -3 | tr '\n' ', ' | sed 's/, $//')
    
    # Extract error/bug fix contexts (clean and filter meaningful content)
    local fix_contexts=$(echo "$diff_content" | grep -E "^[-+].*error|^[-+].*bug|^[-+].*fix" | head -2 | sed 's/^[+-][[:space:]]*//' | grep -v "^[[:space:]]*$" | tr '\n' '; ' | sed 's/; $//')
    
    # Extract specific technical changes from diff for precise commit messages
    local technical_changes=""
    
    # Get AI context for better intent understanding
    local ai_context_for_analysis=$(detect_ai_context)
    local ai_prompt=$(echo "$ai_context_for_analysis" | cut -d'|' -f1)
    
    # Detect regex pattern fixes
    if echo "$diff_content" | grep -q "^-.*grep.*-q[^E]" && echo "$diff_content" | grep -q "^+.*grep.*-qE"; then
        technical_changes="fix broken regex pattern by adding -E flag for extended regex support"
    elif echo "$diff_content" | grep -q "^-.*grep.*-c[^E]" && echo "$diff_content" | grep -q "^+.*grep.*-cE"; then
        technical_changes="fix regex counting by enabling extended regex with -E flag"
    # Detect whitespace/parsing fixes in shell commands
    elif echo "$diff_content" | grep -q "^-.*wc -l[^|]" && echo "$diff_content" | grep -q "^+.*wc -l | tr -d"; then
        technical_changes="fix file count parsing by stripping whitespace from wc command output"
    elif echo "$diff_content" | grep -q "^-.*\$(.*| wc" && echo "$diff_content" | grep -q "^+.*\$(.*| wc.*| tr"; then
        technical_changes="resolve counting issues by cleaning whitespace from command output"
    # Detect function parameter and logic changes
    elif echo "$diff_content" | grep -q "^-.*function.*().*{" && echo "$diff_content" | grep -q "^+.*function.*().*{"; then
        local func_name=$(echo "$diff_content" | grep "^[+-].*function" | head -1 | sed -E 's/.*function[[:space:]]+([a-zA-Z_][a-zA-Z0-9_]*).*/\1/')
        technical_changes="refactor $func_name function signature and parameter handling"
    # Detect integer comparison fixes
    elif echo "$diff_content" | grep -q "^-.*\[\[.*-gt" && echo "$diff_content" | grep -q "^+.*\[\[.*-eq"; then
        technical_changes="fix integer comparison logic from greater-than to equality check"
    elif echo "$diff_content" | grep -q "^-.*\[\[.*-eq" && echo "$diff_content" | grep -q "^+.*\[\[.*-gt"; then
        technical_changes="fix integer comparison logic from equality to greater-than check"
    # Detect variable expansion and quoting fixes
    elif echo "$diff_content" | grep -q "^-.*\$[a-zA-Z_]" && echo "$diff_content" | grep -q "^+.*\"\$[a-zA-Z_]"; then
        technical_changes="fix variable expansion by adding proper shell quoting"
    elif echo "$diff_content" | grep -q "^-.*\$(.*)" && echo "$diff_content" | grep -q "^+.*\"\$(.*)\"\|^+.*\`.*\`"; then
        technical_changes="fix command substitution with proper quoting to handle spaces"
    # Detect control flow improvements
    elif echo "$diff_content" | grep -q "^-.*if.*then" && echo "$diff_content" | grep -q "^+.*case.*in"; then
        technical_changes="refactor conditional logic from if-then to case statement for better readability"
    elif echo "$diff_content" | grep -q "^-.*while.*do" && echo "$diff_content" | grep -q "^+.*for.*in"; then
        technical_changes="optimize loop structure from while to for-in for better performance"
    # Detect automation and staging improvements
    elif echo "$diff_content" | grep -q "^-.*manual.*staging\|^-.*git add" && echo "$diff_content" | grep -q "^+.*auto.*add\|^+.*git add \."; then
        technical_changes="remove manual staging requirement and implement automatic git add functionality"
    elif echo "$diff_content" | grep -q "^-.*read -p" && echo "$diff_content" | grep -q "^+.*fast_mode.*true"; then
        technical_changes="replace interactive prompts with automated fast mode processing"
    # Detect flag and parameter parsing improvements
    elif echo "$diff_content" | grep -q "^+.*--fast" && echo "$diff_content" | grep -q "^+.*fast_mode.*=.*true"; then
        technical_changes="implement --fast flag parameter parsing with mode activation logic"
    elif echo "$diff_content" | grep -q "^+.*-[a-z].*)" && echo "$diff_content" | grep -q "^+.*shift"; then
        technical_changes="add command-line argument parsing with proper parameter shifting"
    # Detect error handling improvements
    elif echo "$diff_content" | grep -q "^-.*exit 1" && echo "$diff_content" | grep -q "^+.*return 1"; then
        technical_changes="fix error handling by using return instead of exit in functions"
    elif echo "$diff_content" | grep -q "^+.*\|\|.*true" && echo "$diff_content" | grep -q "^-.*grep"; then
        technical_changes="add error handling with || true to prevent grep failures"
    # Detect string manipulation and cleanup fixes
    elif echo "$diff_content" | grep -q "^-.*sed 's/.*//'" && echo "$diff_content" | grep -q "^+.*sed.*'s/.*$//'"; then
        technical_changes="fix sed pattern for proper string cleanup and trailing character removal"
    elif echo "$diff_content" | grep -q "^+.*sed.*'s/[{}();|]//g'" || echo "$diff_content" | grep -q "^+.*sed.*'s/IFS=.*//g'"; then
        technical_changes="add string sanitization to remove code fragments from extracted contexts"
    # Detect diff analysis improvements  
    elif echo "$diff_content" | grep -q "^+.*generate.*smart.*commit" && echo "$diff_content" | grep -q "^+.*diff.*analysis"; then
        technical_changes="enhance commit message generation with deep diff content analysis"
    elif echo "$diff_content" | grep -q "^+.*extract.*specific.*changes" && echo "$diff_content" | grep -q "^+.*technical.*details"; then
        technical_changes="implement technical change extraction for precise commit message generation"
    # Use AI prompt context for additional specificity
    elif [ -n "$ai_prompt" ]; then
        if echo "$ai_prompt" | grep -q "fix.*issue.*files.*detected" && echo "$diff_content" | grep -q "^+.*tr -d"; then
            technical_changes="fix file detection issues by cleaning whitespace from command output"
        elif echo "$ai_prompt" | grep -q "make.*work.*fast.*mode" && echo "$diff_content" | grep -q "^+.*--fast"; then
            technical_changes="implement fast mode parameter parsing and automated workflow"
        elif echo "$ai_prompt" | grep -q "specific.*commit.*message" && echo "$diff_content" | grep -q "^+.*technical.*analysis"; then
            technical_changes="implement precise commit message generation using technical diff analysis"
        elif echo "$ai_prompt" | grep -q "automatic.*staging" && echo "$diff_content" | grep -q "^+.*git add"; then
            technical_changes="implement automatic staging to eliminate manual git add requirement"
        fi
    fi
    
    # Generate highly specific subject lines based on actual changes
    case "$commit_type" in
        "feat")
            # Use specific technical analysis for precise feature descriptions
            if [ -n "$technical_changes" ] && echo "$technical_changes" | grep -q "implement\|add"; then
                subject="$technical_changes"
            elif [ -n "$new_function_names" ] && [ "$added_functions" -gt 0 ]; then
                if [ "$added_functions" -eq 1 ]; then
                    subject="add $new_function_names function"
                else
                    subject="add $added_functions new functions ($new_function_names)"
                fi
            elif [ -n "$new_options" ] && [ "$added_parameters" -gt 0 ]; then
                if [ "$added_parameters" -eq 1 ]; then
                    subject="add $new_options command-line option"
                else
                    subject="add $added_parameters new command-line options ($new_options)"
                fi
            elif echo "$diff_content" | grep -q "^+.*--fast.*mode\|^+.*fast_mode.*=.*true"; then
                subject="implement fast mode for automated commits without prompts"
            elif echo "$diff_content" | grep -q "^+.*auto.*push\|^+.*git push"; then
                subject="add automatic push capability for streamlined workflow"
            elif echo "$diff_content" | grep -q "^+.*auto.*stage\|^+.*git add"; then
                subject="implement automatic staging to eliminate manual git add"
            elif echo "$diff_content" | grep -q "^+.*commit.*message.*generation\|^+.*generate.*smart"; then
                subject="enhance commit message generation with deep diff analysis"
            elif echo "$diff_content" | grep -q "^+.*AI.*context\|^+.*prompt.*logging"; then
                subject="add AI context and prompt detection for better tracking"
            elif echo "$diff_content" | grep -q "^+.*alias\|^+.*\.bashrc\|^+.*\.zshrc"; then
                subject="add shell aliases for improved development workflow"
            elif echo "$diff_content" | grep -q "^+.*workflow\|^+.*\.github.*actions"; then
                subject="implement GitHub Actions CI/CD automation"
            elif echo "$diff_content" | grep -q "^+.*ontology.*processing\|^+.*cultural.*analysis"; then
                subject="expand cultural ontology processing capabilities"
            elif echo "$diff_content" | grep -q "^+.*rag.*system\|^+.*retrieval"; then
                subject="enhance OG-RAG system with advanced retrieval features"
            elif echo "$diff_content" | grep -q "^+.*proverb.*translation\|^+.*kikuyu"; then
                subject="add Kikuyu proverb processing and translation support"
            elif [ "$added_classes" -gt 0 ]; then
                subject="add $added_classes new class$([ "$added_classes" -gt 1 ] && echo "es") for enhanced functionality"
            elif [ "$added_tests" -gt 0 ]; then
                subject="add $added_tests test cases for improved coverage"
            else
                # Fallback to file-based detection
                local primary_file=$(echo "$staged_files" | head -1 | sed 's|.*/||' | sed 's/\.[^.]*$//')
                subject="implement new functionality in $primary_file"
            fi
            ;;
        "fix")
            # Use specific technical analysis for precise commit messages
            if [ -n "$technical_changes" ]; then
                subject="$technical_changes"
            elif echo "$staged_files" | grep -q "ai-smart-commit\.sh" && [ -n "$content_context" ]; then
                # We're fixing the smart commit script itself
                subject="fix $content_context"
            elif [ -n "$fix_contexts" ] && [ "$fixed_errors" -gt 0 ]; then
                # Clean and filter fix contexts to avoid code fragments
                local clean_contexts=$(echo "$fix_contexts" | sed 's/[{}();|]//g' | sed 's/IFS=.*//g' | sed 's/read -r.*//g')
                if echo "$clean_contexts" | grep -q "bash.*syntax\|integer.*comparison\|syntax.*error"; then
                    subject="resolve bash syntax and scripting issues"
                elif echo "$clean_contexts" | grep -q "error.*handling\|exception\|validation"; then
                    subject="improve error handling and exception management"
                elif echo "$clean_contexts" | grep -q "prompt.*handling\|interactive\|input"; then
                    subject="fix interactive prompt handling and user input validation"
                elif echo "$clean_contexts" | grep -q "git.*operation\|repository\|commit"; then
                    subject="resolve git repository operation failures"
                elif echo "$diff_content" | grep -q "^+.*generate.*smart.*commit\|^+.*diff.*analysis"; then
                    subject="enhance commit message generation logic and diff analysis"
                else
                    subject="resolve critical functionality issues"
                fi
            elif echo "$diff_content" | grep -q "^-.*manual\|^+.*automatic"; then
                subject="replace manual processes with automated alternatives"
            elif echo "$diff_content" | grep -q "^-.*deprecated\|^+.*updated"; then
                subject="update deprecated code to use modern alternatives"
            elif echo "$diff_content" | grep -q "^-.*hardcoded\|^+.*configurable"; then
                subject="replace hardcoded values with configurable options"
            else
                local primary_file=$(echo "$staged_files" | head -1 | sed 's|.*/||' | sed 's/\.[^.]*$//')
                subject="resolve issues in $primary_file"
            fi
            ;;
        "docs")
            # Use extracted content context for highly specific commit messages
            local specific_context="$content_context"
            
            if echo "$staged_files" | grep -q "ai-smart-commit\.sh"; then
                # We're documenting or changing the smart commit script itself
                subject="enhance smart commit system with $specific_context"
            elif echo "$staged_files" | grep -q "chapters.*README" && [ -n "$specific_context" ]; then
                subject="add $specific_context"
            elif echo "$staged_files" | grep -q "README" && echo "$diff_content" | grep -q "^+.*#.*Usage\|^+.*#.*Examples"; then
                if [ -n "$specific_context" ]; then
                    subject="add $specific_context"
                else
                    subject="add comprehensive usage examples and configuration guide"
                fi
            elif echo "$staged_files" | grep -q "README" && echo "$diff_content" | grep -q "^+.*test.*comment"; then
                subject="add test comments to demonstrate enhanced functionality"
            elif echo "$staged_files" | grep -q "SMART-COMMIT.*README"; then
                subject="create comprehensive smart commit system documentation"
            elif echo "$staged_files" | grep -q "docs/thesis/" && echo "$diff_content" | grep -q "^+.*\\\\chapter\|^+.*\\\\section"; then
                subject="add new thesis chapter and section structure"
            elif echo "$staged_files" | grep -q "docs/thesis/" && echo "$diff_content" | grep -q "^+.*\\\\cite\|^+.*\\\\ref"; then
                subject="enhance thesis with additional citations and references"
            elif echo "$staged_files" | grep -q "\.md$" && [ "$(echo "$staged_files" | wc -l | tr -d ' ')" -gt 1 ]; then
                local doc_count=$(echo "$staged_files" | grep -c "\.md$")
                if [ -n "$specific_context" ]; then
                    subject="update $doc_count documentation files with $specific_context"
                else
                    subject="update $doc_count documentation files with latest information"
                fi
            elif echo "$diff_content" | grep -q "^+.*API.*documentation\|^+.*function.*description"; then
                subject="enhance API documentation with detailed function descriptions"
            else
                local primary_doc=$(echo "$staged_files" | head -1 | sed 's|.*/||' | sed 's/\.[^.]*$//')
                if [ -n "$specific_context" ]; then
                    subject="improve $primary_doc with $specific_context"
                else
                    subject="improve $primary_doc documentation"
                fi
            fi
            ;;
        "chore")
            if echo "$staged_files" | grep -q "package\.json\|requirements\|Pipfile" && [ "$config_changes" -gt 0 ]; then
                subject="update project dependencies and package requirements"
            elif echo "$staged_files" | grep -q "\.github.*ISSUE_TEMPLATE"; then
                subject="add comprehensive GitHub issue templates for project management"
            elif echo "$staged_files" | grep -q "\.github.*workflows" && echo "$diff_content" | grep -q "^+.*on:.*push\|^+.*jobs:"; then
                subject="configure GitHub Actions workflow automation"
            elif echo "$diff_content" | grep -q "^+.*alias.*smart.*commit\|^+.*export.*PATH"; then
                subject="configure shell aliases and environment for development workflow"
            elif echo "$staged_files" | grep -q "setup.*\.sh" && echo "$diff_content" | grep -q "^+.*install\|^+.*configure"; then
                subject="enhance automated project setup and configuration scripts"
            elif [ "$(echo "$staged_files" | wc -l | tr -d ' ')" -gt 5 ]; then
                subject="reorganize project structure and update multiple configuration files"
            else
                subject="maintain project configuration and development environment"
            fi
            ;;
        "refactor")
            if [ -n "$technical_changes" ] && echo "$technical_changes" | grep -q "refactor\|optimize"; then
                subject="$technical_changes"
            else
                local primary_file=$(echo "$staged_files" | head -1 | sed 's|.*/||' | sed 's/\.[^.]*$//')
                subject="refactor $primary_file for improved maintainability and performance"
            fi
            ;;
        "test")
            if [ "$added_tests" -gt 0 ]; then
                subject="add $added_tests test cases for improved code coverage"
            else
                subject="enhance test coverage and validation framework"
            fi
            ;;
        *)
            # Smart fallback with actual file analysis
            local primary_file=$(echo "$staged_files" | head -1 | sed 's|.*/||' | sed 's/\.[^.]*$//')
            if [ "$added_functions" -gt 0 ] || [ "$added_methods" -gt 0 ]; then
                subject="enhance $primary_file with $((added_functions + added_methods)) new functions"
            elif [ "$config_changes" -gt 0 ]; then
                subject="update $primary_file configuration and settings"
            else
                subject="modify $primary_file with system improvements"
            fi
            ;;
    esac
    
    # Generate comprehensive body with detailed metrics
    local file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
    local new_files=$(git diff --cached --diff-filter=A --name-only | wc -l | tr -d ' ')
    local modified_files=$(git diff --cached --diff-filter=M --name-only | wc -l | tr -d ' ')
    local deleted_files=$(git diff --cached --diff-filter=D --name-only | wc -l | tr -d ' ')
    local lines_added=$(echo "$diff_content" | grep -c "^+")
    local lines_removed=$(echo "$diff_content" | grep -c "^-")
    
    # Build detailed body with metrics
    body="Modified $file_count file$([ "$file_count" -gt 1 ] && echo "s")"
    
    # Add file change breakdown
    local changes=""
    [ "$new_files" -gt 0 ] && changes+="$new_files new"
    [ "$modified_files" -gt 0 ] && [ -n "$changes" ] && changes+=", $modified_files modified"
    [ "$modified_files" -gt 0 ] && [ -z "$changes" ] && changes+="$modified_files modified"
    [ "$deleted_files" -gt 0 ] && [ -n "$changes" ] && changes+=", $deleted_files deleted"
    [ "$deleted_files" -gt 0 ] && [ -z "$changes" ] && changes+="$deleted_files deleted"
    
    [ -n "$changes" ] && body+=" ($changes)"
    
    # Add line change metrics
    if [ "$lines_added" -gt 0 ] || [ "$lines_removed" -gt 0 ]; then
        body+=". Changes: +$lines_added/-$lines_removed lines"
    fi
    
    # Add specific improvement details
    local improvements=""
    [ "$added_functions" -gt 0 ] && improvements+="$added_functions functions"
    [ "$added_methods" -gt 0 ] && [ -n "$improvements" ] && improvements+=", $added_methods methods"
    [ "$added_methods" -gt 0 ] && [ -z "$improvements" ] && improvements+="$added_methods methods"
    [ "$added_classes" -gt 0 ] && [ -n "$improvements" ] && improvements+=", $added_classes classes"
    [ "$added_classes" -gt 0 ] && [ -z "$improvements" ] && improvements+="$added_classes classes"
    [ "$added_parameters" -gt 0 ] && [ -n "$improvements" ] && improvements+=", $added_parameters CLI options"
    [ "$added_parameters" -gt 0 ] && [ -z "$improvements" ] && improvements+="$added_parameters CLI options"
    [ "$added_tests" -gt 0 ] && [ -n "$improvements" ] && improvements+=", $added_tests tests"
    [ "$added_tests" -gt 0 ] && [ -z "$improvements" ] && improvements+="$added_tests tests"
    
    [ -n "$improvements" ] && body+=". Added: $improvements"
    
    # Add file list for small changesets
    if [ "$file_count" -le 3 ]; then
        local file_list=$(echo "$staged_files" | sed 's|.*/||' | tr '\n' ', ' | sed 's/, $//')
        body+=". Files: $file_list"
    fi
    
    # Get AI context for prompt incorporation
    local ai_context_for_body=$(detect_ai_context)
    local ai_prompt_for_body=$(echo "$ai_context_for_body" | cut -d'|' -f1)
    
    # Add prompt context if available and meaningful
    if [ -n "$ai_prompt_for_body" ] && [ ${#ai_prompt_for_body} -gt 20 ]; then
        # Truncate very long prompts for readability
        local prompt_summary="$ai_prompt_for_body"
        if [ ${#prompt_summary} -gt 100 ]; then
            prompt_summary="$(echo "$prompt_summary" | cut -c1-97)..."
        fi
        body+=". Prompt: $prompt_summary"
    fi
    
    body+=". Generated by thiLLMo AI-enhanced commit system"
    
    # Format final commit message with scope
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
    
    # Detect AI context with enhanced prompt inference
    local ai_context=$(detect_ai_context)
    IFS='|' read -r inferred_prompt context assistant model <<< "$ai_context"
    
    # Build full commit message with AI context
    local full_commit_msg="$commit_msg

$commit_body"
    
    # Add AI context fields (following conventional commit format)
    if [ -n "$inferred_prompt" ] || [ -n "$context" ] || [ -n "$assistant" ] || [ -n "$model" ]; then
        full_commit_msg+="

"
        [ -n "$inferred_prompt" ] && full_commit_msg+="Actual-prompt: $inferred_prompt
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
    
    # Detect AI context with enhanced inference
    local ai_context=$(detect_ai_context)
    IFS='|' read -r inferred_prompt context assistant model <<< "$ai_context"
    
    # Pre-fill commitizen environment variables for auto-population
    export CZ_PRE_COMMIT_TYPE="$suggested_type"
    export CZ_PRE_ASSISTANT="$assistant"
    export CZ_PRE_MODEL="$model"
    export CZ_PRE_CONTEXT="$context"
    export CZ_PRE_PROMPT="$inferred_prompt"
    
    # Display detected AI context
    if [ -n "$inferred_prompt" ] || [ -n "$context" ]; then
        echo -e "${CYAN}🤖 Detected AI Context:${NC}"
        [ -n "$assistant" ] && echo "   Assistant: $assistant"
        [ -n "$model" ] && echo "   Model: $model"
        [ -n "$context" ] && echo "   Context: $context"
        [ -n "$inferred_prompt" ] && echo "   Inferred Prompt: $inferred_prompt"
        echo
    fi
    
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
  -q, --quick      Quick mode (skip prompts, auto-stage is default)
  -f, --fast       Fast mode (auto-generate commit, no interaction)
  -p, --push       Auto-push after successful commit
  -v, --verbose    Verbose output (default)
  -s, --silent     Minimal output
  -c, --config     Show current configuration
  --history        Show recent commit history

${CYAN}Core Philosophy:${NC}
  🔄 Automatically stages all changes (git add .)
  🤖 AI-powered commit message generation
  ✅ Only prompts for push confirmation (unless -p used)

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
  $0 -q                # Quick commit (skip prompts)
  $0 -qp               # Quick commit and auto-push
  $0 -f                # Fast auto-generated commit
  $0 -fp               # Fast commit and auto-push
  $0 --config          # Show current configuration

${CYAN}Mode Comparison:${NC}
  ${GREEN}Interactive${NC}  - Full commitizen prompt with AI suggestions (auto-stages)
  ${YELLOW}Quick${NC}        - Skip prompts, interactive commit only (auto-stages)
  ${PURPLE}Fast${NC}         - Fully automated commit with smart defaults (auto-stages)

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
                shift
                ;;
            -f|--fast)
                fast_mode=true
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
    
    # Auto-stage all changes (core philosophy: automate add, commit, push cycle)
    git add .
    if [ "$fast_mode" = true ]; then
        echo -e "${GREEN}📁 All changes staged for fast commit${NC}"
    else
        echo -e "${GREEN}📁 All changes staged automatically${NC}"
    fi
    
    # Show current status for transparency
    echo -e "${BLUE}📋 Repository status after staging:${NC}"
    git status --short
    echo
    
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
# Test technical change detection
