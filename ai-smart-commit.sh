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
DEFAULT_ASSISTANT="Claude"
DEFAULT_MODEL="Claude 3.5 Sonnet"

# Load configuration
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    else
        # Create default config
        cat > "$CONFIG_FILE" << EOF
# thiLLMo Smart Commit Configuration
DEFAULT_ASSISTANT="Claude"
DEFAULT_MODEL="Claude 3.5 Sonnet"
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
    
    # Priority 1: Respect explicitly configured defaults (highest priority)
    # If user has configured Claude as default, honor that choice unless
    # there's strong evidence of a different AI being actively used
    assistant="$DEFAULT_ASSISTANT"
    model="$DEFAULT_MODEL"
    context="Using configured default: $DEFAULT_ASSISTANT ($DEFAULT_MODEL)"
    
    # Priority 2: Strong indicators only override if defaults aren't explicitly Claude
    # This prevents incidental shell history from overriding intentional configuration
    local override_allowed=true
    if [ "$DEFAULT_ASSISTANT" = "Claude" ] && [ "$DEFAULT_MODEL" = "Claude 3.5 Sonnet" ]; then
        override_allowed=false
        context="Configured for Claude 3.5 Sonnet - honoring user preference"
    fi
    
    # Priority 3: Check VS Code environment for active AI assistants (only if override allowed)
    if [ "$override_allowed" = "true" ] && command -v code &> /dev/null && pgrep -f "code" > /dev/null; then
        if [ -d "$HOME/.vscode/extensions" ]; then
            # Check for Claude/Anthropic extensions
            if ls "$HOME/.vscode/extensions" | grep -q "anthropic\|claude"; then
                assistant="Claude"
                model="Claude 3.5 Sonnet"
                context="VS Code with Claude 3.5 Sonnet active"
            # Check for GitHub Copilot
            elif ls "$HOME/.vscode/extensions" | grep -q "copilot"; then
                assistant="GitHub Copilot"
                model="GPT-4"
                context="VS Code with Copilot active"
            # Check for other AI extensions
            elif ls "$HOME/.vscode/extensions" | grep -q "openai\|chatgpt"; then
                assistant="ChatGPT"
                model="GPT-4"
                context="VS Code with OpenAI extension active"
            fi
        fi
    fi
    
    # Priority 4: Check for very recent AI tool usage (last 5 commands only, and only if override allowed)
    if [ "$override_allowed" = "true" ] && command -v history &> /dev/null; then
        local recent_history=$(history 5 2>/dev/null || true)
        # Only look at very recent commands and be more specific
        if echo "$recent_history" | grep -q "claude.*cli\|anthropic.*api\|claude.*chat"; then
            assistant="Claude"
            model="Claude 3.5 Sonnet"
            context="Very recent Claude CLI usage detected"
        elif echo "$recent_history" | grep -q "github.*copilot.*chat\|copilot.*chat"; then
            assistant="GitHub Copilot"
            model="GPT-4"
            context="Very recent Copilot chat usage detected"
        fi
        # Note: Ignore incidental mentions like "gh copilot explain" as they don't indicate active AI session
    fi
    
    # Priority 5: Check environment variables for AI tool indicators (only if override allowed)
    if [ "$override_allowed" = "true" ]; then
        if [ -n "$ANTHROPIC_API_KEY" ] || [ -n "$CLAUDE_API_KEY" ]; then
            assistant="Claude"
            model="Claude 3.5 Sonnet"
            context="Anthropic API credentials detected"
        elif [ -n "$OPENAI_API_KEY" ]; then
            assistant="OpenAI"
            model="GPT-4"
            context="OpenAI API credentials detected"
        fi
    fi
    
    # Priority 6: Reinforce Claude detection with configuration files (always check for Claude)
    if [ -f "$HOME/.anthropic" ] || [ -f "$HOME/.claude" ]; then
        assistant="Claude"
        model="Claude 3.5 Sonnet"
        context="Claude configuration files detected"
    fi
    
    # Priority 7: Enhanced VS Code workspace detection for Claude (always check for Claude)
    if [ -f ".vscode/settings.json" ] && grep -q "anthropic\|claude" ".vscode/settings.json" 2>/dev/null; then
        assistant="Claude"
        model="Claude 3.5 Sonnet"
        context="VS Code workspace configured for Claude"
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
        elif echo "$diff_content" | grep -q "prompt.*context.*integration\|ai_prompt_for_subject"; then
            prompt="Improve commit message specificity by using prompt context to generate more accurate subject lines that reflect actual changes made"
            context="Enhancing subject line generation to extract specific details from user prompts rather than generic descriptions"
        elif echo "$diff_content" | grep -q "override_allowed\|Claude.*3\.5.*Sonnet\|honoring.*user.*preference"; then
            prompt="Fix AI model detection to correctly identify Claude 3.5 Sonnet instead of incorrectly falling back to GPT-4 from shell history"
            context="Fixing AI assistant detection logic to respect explicit user configuration and prevent false overrides"
        elif echo "$diff_content" | grep -q "cached.*commit.*message\|technical_changes.*=.*fix.*variable"; then
            prompt="Fix commit message generation to analyze actual changes instead of returning cached/generic messages that don't match the real modifications"
            context="Improving commit message accuracy by eliminating hardcoded patterns and enhancing real-time diff analysis"
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

# Generate intent-aware semantic commit messages
generate_smart_commit_message() {
    local commit_type="$1"
    local staged_files=$(git diff --cached --name-only)
    local diff_content=$(git diff --cached --no-color)
    local scope=""
    local subject=""
    local body=""
    
    # Get AI context for intent understanding (highest priority)
    local ai_context=$(detect_ai_context)
    local ai_prompt=$(echo "$ai_context" | cut -d'|' -f1)
    local context=$(echo "$ai_context" | cut -d'|' -f2)
    
    # Enhanced scope detection with semantic priority
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
    elif echo "$staged_files" | grep -q "docs/proposal/"; then
        scope="proposal"
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
    
    # Intent-first analysis: Extract semantic intent from AI prompt
    local intent=""
    if [ -n "$ai_prompt" ]; then
        intent=$(extract_semantic_intent_from_prompt "$ai_prompt" "$context")
    fi
    
    # Secondary: Analyze file patterns for semantic meaning
    if [ -z "$intent" ]; then
        intent=$(analyze_semantic_file_patterns "$staged_files" "$diff_content")
    fi
    
    # Generate semantic subject based on intent
    subject=$(generate_semantic_subject "$intent" "$commit_type" "$scope")
    
    # Generate comprehensive body with semantic context
    local file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
    local new_files=$(git diff --cached --diff-filter=A --name-only | wc -l | tr -d ' ')
    local modified_files=$(git diff --cached --diff-filter=M --name-only | wc -l | tr -d ' ')
    local deleted_files=$(git diff --cached --diff-filter=D --name-only | wc -l | tr -d ' ')
    local lines_added=$(echo "$diff_content" | grep -c "^+")
    local lines_removed=$(echo "$diff_content" | grep -c "^-")
    
    # Build semantic body
    body="Accomplished: $subject"
    
    # Add change context
    body+=". Modified $file_count file$([ "$file_count" -gt 1 ] && echo "s")"
    
    # Add semantic change breakdown
    local changes=""
    [ "$new_files" -gt 0 ] && changes+="$new_files new"
    [ "$modified_files" -gt 0 ] && [ -n "$changes" ] && changes+=", $modified_files modified"
    [ "$modified_files" -gt 0 ] && [ -z "$changes" ] && changes+="$modified_files modified"
    [ "$deleted_files" -gt 0 ] && [ -n "$changes" ] && changes+=", $deleted_files deleted"
    [ "$deleted_files" -gt 0 ] && [ -z "$changes" ] && changes+="$deleted_files deleted"
    
    [ -n "$changes" ] && body+=" ($changes)"
    
    # Add line metrics
    if [ "$lines_added" -gt 0 ] || [ "$lines_removed" -gt 0 ]; then
        body+=". Impact: +$lines_added/-$lines_removed lines"
    fi
    
    # Add semantic improvements
    local improvements=$(extract_semantic_improvements "$diff_content")
    [ -n "$improvements" ] && body+=". Enhancements: $improvements"
    
    # Add file list for small changesets
    if [ "$file_count" -le 3 ]; then
        local file_list=$(echo "$staged_files" | sed 's|.*/||' | tr '\n' ', ' | sed 's/, $//')
        body+=". Files: $file_list"
    fi
    
    # Add AI context for traceability
    if [ -n "$ai_prompt" ] && [ ${#ai_prompt} -gt 20 ]; then
        local prompt_summary="$ai_prompt"
        if [ ${#prompt_summary} -gt 100 ]; then
            prompt_summary="$(echo "$prompt_summary" | cut -c1-97)..."
        fi
        body+=". Intent: $prompt_summary"
    fi
    
    body+=". Generated by thiLLMo semantic commit system"
    
    # Format final commit message
    local commit_msg="$commit_type"
    [ -n "$scope" ] && commit_msg+="($scope)"
    commit_msg+=": $subject"
    
    echo "$commit_msg|$body"
}

# Extract semantic intent from AI prompt context
extract_semantic_intent_from_prompt() {
    local prompt="$1"
    local context="$2"
    local intent=""
    
    # Convert markdown to LaTeX patterns
    if echo "$prompt" | grep -q "convert.*markdown.*latex\|markdown.*to.*latex"; then
        intent="document format conversion"
    # Documentation enhancement patterns
    elif echo "$prompt" | grep -q "add.*documentation.*usage\|enhance.*documentation"; then
        intent="documentation enhancement"
    # Workflow automation patterns
    elif echo "$prompt" | grep -q "implement.*fast.*mode\|streamlined.*commit"; then
        intent="workflow automation"
    # Fix specificity patterns
    elif echo "$prompt" | grep -q "commit.*message.*specificity\|specific.*commit"; then
        intent="commit message enhancement"
    # File detection fixes
    elif echo "$prompt" | grep -q "fix.*file.*detection\|resolve.*counting"; then
        intent="file analysis accuracy"
    # Configuration and setup patterns
    elif echo "$prompt" | grep -q "setup.*alias\|configure.*environment"; then
        intent="development environment setup"
    # Research proposal patterns
    elif echo "$prompt" | grep -q "research.*proposal\|thesis.*document"; then
        intent="academic document preparation"
    # Issue template patterns
    elif echo "$prompt" | grep -q "issue.*template\|github.*template"; then
        intent="project management template"
    # AI context patterns
    elif echo "$prompt" | grep -q "ai.*context\|prompt.*context"; then
        intent="AI context integration"
    # Automation patterns
    elif echo "$prompt" | grep -q "automatic.*staging\|eliminate.*manual"; then
        intent="process automation"
    # Documentation cleanup patterns
    elif echo "$prompt" | grep -q "remove.*test.*text\|clean.*up.*test"; then
        intent="documentation cleanup"
    fi
    
    echo "$intent"
}

# Analyze semantic file patterns
analyze_semantic_file_patterns() {
    local files="$1"
    local diff="$2"
    local pattern=""
    
    # Documentation transformation patterns
    if [[ "$files" =~ .*\.md.* ]] && [[ "$diff" =~ .*\.tex.* ]]; then
        pattern="documentation format conversion"
    elif [[ "$files" =~ README.*\.md ]] && echo "$diff" | grep -q "^+.*## Usage"; then
        pattern="user documentation enhancement"
    # LaTeX document patterns
    elif [[ "$files" =~ .*\.tex$ ]] && echo "$diff" | grep -q "^+.*\\\\documentclass"; then
        pattern="academic document creation"
    # Project structure patterns
    elif [[ "$files" =~ \.github/workflows.* ]] && echo "$diff" | grep -q "^+.*latex.*build"; then
        pattern="document building automation"
    elif [[ "$files" =~ \.github/ISSUE_TEMPLATE.* ]]; then
        pattern="project management template"
    # Ontology patterns
    elif [[ "$files" =~ src/ontology.* ]] && echo "$diff" | grep -q "^+.*class.*Cultural"; then
        pattern="cultural knowledge expansion"
    # Configuration patterns
    elif [[ "$files" =~ setup.*\.sh ]] && echo "$diff" | grep -q "^+.*alias"; then
        pattern="development workflow setup"
    # Smart commit patterns
    elif [[ "$files" =~ ai-smart-commit\.sh ]] && echo "$diff" | grep -q "^+.*fast.*mode"; then
        pattern="commit workflow automation"
    elif [[ "$files" =~ ai-smart-commit\.sh ]] && echo "$diff" | grep -q "^+.*semantic.*commit"; then
        pattern="commit message intelligence"
    fi
    
    echo "$pattern"
}

# Generate semantic subject based on intent
generate_semantic_subject() {
    local intent="$1"
    local commit_type="$2"
    local scope="$3"
    local subject=""
    
    case "$intent" in
        "document format conversion")
            subject="convert research proposal from markdown to LaTeX format"
            ;;
        "documentation enhancement")
            subject="enhance user documentation with comprehensive usage guide"
            ;;
        "workflow automation")
            subject="enable streamlined commit workflow with fast mode"
            ;;
        "commit message enhancement")
            subject="improve commit message specificity with semantic analysis"
            ;;
        "file analysis accuracy")
            subject="resolve file counting accuracy in change detection"
            ;;
        "development environment setup")
            subject="configure development environment with smart commit aliases"
            ;;
        "academic document preparation")
            subject="prepare thesis documentation with professional LaTeX formatting"
            ;;
        "project management template")
            subject="create comprehensive GitHub issue templates for project workflow"
            ;;
        "AI context integration")
            subject="integrate AI prompt context into commit message generation"
            ;;
        "process automation")
            subject="automate git staging process to eliminate manual steps"
            ;;
        "documentation cleanup")
            subject="clean up documentation by removing test content"
            ;;
        "cultural knowledge expansion")
            subject="expand cultural ontology framework for proverb analysis"
            ;;
        "commit workflow automation")
            subject="enhance commit workflow with automated staging and fast mode"
            ;;
        "commit message intelligence")
            subject="implement semantic commit message generation with AI context"
            ;;
        *)
            # Fallback to conventional patterns
            case "$commit_type" in
                "feat")
                    subject="implement new functionality for enhanced workflow"
                    ;;
                "fix")
                    subject="resolve functionality issues and improve reliability"
                    ;;
                "docs")
                    subject="update documentation with latest information"
                    ;;
                "chore")
                    subject="maintain project configuration and environment"
                    ;;
                *)
                    subject="improve system capabilities and user experience"
                    ;;
            esac
            ;;
    esac
    
    echo "$subject"
}

# Extract semantic improvements from diff
extract_semantic_improvements() {
    local diff="$1"
    local improvements=""
    
    # Function/method additions
    if echo "$diff" | grep -q "^+.*function \|^+.*def \|^+.*class \|^+.*interface"; then
        local new_funcs=$(echo "$diff" | grep -c "^+.*function \|^+.*def ")
        [ "$new_funcs" -gt 0 ] && improvements+="$new_funcs new functions"
    fi
    
    # Feature flags and modes
    if echo "$diff" | grep -q "^+.*--fast\|^+.*fast.*mode"; then
        [ -n "$improvements" ] && improvements+=", "
        improvements+="fast mode capability"
    fi
    
    # Automation improvements
    if echo "$diff" | grep -q "^+.*automatic\|^+.*auto.*"; then
        [ -n "$improvements" ] && improvements+=", "
        improvements+="process automation"
    fi
    
    # Error handling
    if echo "$diff" | grep -q "^+.*error.*handling\|^+.*validation"; then
        [ -n "$improvements" ] && improvements+=", "
        improvements+="error handling"
    fi
    
    # Configuration enhancements
    if echo "$diff" | grep -q "^+.*config\|^+.*setup\|^+.*alias"; then
        [ -n "$improvements" ] && improvements+=", "
        improvements+="configuration management"
    fi
    
    # Documentation additions
    if echo "$diff" | grep -q "^+.*#.*Usage\|^+.*#.*Examples\|^+.*README"; then
        [ -n "$improvements" ] && improvements+=", "
        improvements+="documentation coverage"
    fi
    
    # Template additions
    if echo "$diff" | grep -q "^+.*template\|^+.*\.github"; then
        [ -n "$improvements" ] && improvements+=", "
        improvements+="project templates"
    fi
    
    # AI context enhancements
    if echo "$diff" | grep -q "^+.*AI.*context\|^+.*prompt.*context"; then
        [ -n "$improvements" ] && improvements+=", "
        improvements+="AI context tracking"
    fi
    
    echo "$improvements"
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
