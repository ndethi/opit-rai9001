#!/bin/bash

# GitHub Issue Automation - Installation and Setup Script
# Cross-platform installer for GitHub CLI and authentication

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
LOG_FILE="$SCRIPT_DIR/setup.log"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Install GitHub CLI based on OS
install_gh_cli() {
    local os=$(detect_os)
    
    echo -e "${BLUE}🔧 Installing GitHub CLI for $os...${NC}"
    
    case $os in
        "macos")
            if command_exists brew; then
                log "Installing GitHub CLI via Homebrew"
                brew install gh
            else
                echo -e "${YELLOW}⚠️  Homebrew not found. Please install it first:${NC}"
                echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                exit 1
            fi
            ;;
        "linux")
            if command_exists apt; then
                log "Installing GitHub CLI via apt"
                curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
                echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
                sudo apt update
                sudo apt install gh
            elif command_exists yum; then
                log "Installing GitHub CLI via yum"
                sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
                sudo dnf install gh
            else
                echo -e "${YELLOW}⚠️  Package manager not supported. Please install GitHub CLI manually:${NC}"
                echo "   https://github.com/cli/cli/releases"
                exit 1
            fi
            ;;
        "windows")
            if command_exists winget; then
                log "Installing GitHub CLI via winget"
                winget install --id GitHub.cli
            elif command_exists choco; then
                log "Installing GitHub CLI via chocolatey"
                choco install gh
            else
                echo -e "${YELLOW}⚠️  Please install GitHub CLI manually from:${NC}"
                echo "   https://github.com/cli/cli/releases"
                exit 1
            fi
            ;;
        *)
            echo -e "${RED}❌ Unsupported operating system: $os${NC}"
            exit 1
            ;;
    esac
    
    log "GitHub CLI installation completed"
}

# Check GitHub CLI authentication
check_auth() {
    echo -e "${BLUE}🔐 Checking GitHub authentication...${NC}"
    
    if gh auth status >/dev/null 2>&1; then
        local user=$(gh api user --jq .login)
        echo -e "${GREEN}✅ Authenticated as: $user${NC}"
        log "GitHub authentication verified for user: $user"
        return 0
    else
        echo -e "${YELLOW}⚠️  Not authenticated with GitHub${NC}"
        return 1
    fi
}

# Authenticate with GitHub
authenticate_github() {
    echo -e "${BLUE}🔑 Setting up GitHub authentication...${NC}"
    
    echo "Please choose authentication method:"
    echo "1) Login via web browser (recommended)"
    echo "2) Login with personal access token"
    echo ""
    read -p "Choose option (1-2): " auth_choice
    
    case $auth_choice in
        1)
            log "Authenticating via web browser"
            gh auth login --web
            ;;
        2)
            log "Authenticating via personal access token"
            gh auth login --with-token
            ;;
        *)
            echo -e "${RED}❌ Invalid choice${NC}"
            exit 1
            ;;
    esac
    
    # Verify authentication
    if check_auth; then
        echo -e "${GREEN}✅ GitHub authentication successful!${NC}"
    else
        echo -e "${RED}❌ GitHub authentication failed${NC}"
        exit 1
    fi
}

# Validate repository access
validate_repository() {
    local repo="$1"
    
    if [[ -z "$repo" ]]; then
        # Try to detect repository from git remote
        if git rev-parse --git-dir >/dev/null 2>&1; then
            local remote_url=$(git remote get-url origin 2>/dev/null || echo "")
            if [[ -n "$remote_url" ]]; then
                # Extract owner/repo from GitHub URL
                repo=$(echo "$remote_url" | sed -E 's|.*github\.com[:/]([^/]+/[^/]+).*|\1|' | sed 's/\.git$//')
            fi
        fi
        
        if [[ -z "$repo" ]]; then
            echo -e "${YELLOW}⚠️  Repository not specified and cannot be auto-detected${NC}"
            read -p "Enter repository (owner/repo): " repo
        fi
    fi
    
    echo -e "${BLUE}🔍 Validating repository access: $repo${NC}"
    
    if gh repo view "$repo" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Repository access confirmed: $repo${NC}"
        log "Repository validation successful: $repo"
        echo "$repo" > "$SCRIPT_DIR/.repository"
        return 0
    else
        echo -e "${RED}❌ Cannot access repository: $repo${NC}"
        echo "Please check:"
        echo "  - Repository exists and is accessible"
        echo "  - You have appropriate permissions"
        echo "  - Repository name is correct (owner/repo format)"
        exit 1
    fi
}

# Check repository settings and features
check_repository_features() {
    local repo="$1"
    
    echo -e "${BLUE}🔍 Checking repository features...${NC}"
    
    # Check if Issues are enabled
    local issues_enabled=$(gh api "repos/$repo" --jq .has_issues)
    if [[ "$issues_enabled" == "true" ]]; then
        echo -e "${GREEN}✅ Issues enabled${NC}"
    else
        echo -e "${YELLOW}⚠️  Issues are disabled for this repository${NC}"
        echo "Please enable Issues in repository settings"
        exit 1
    fi
    
    # Check if Projects are available
    if gh api "repos/$repo/projects" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Projects available${NC}"
    else
        echo -e "${YELLOW}⚠️  Projects may not be available${NC}"
    fi
    
    log "Repository features validated for: $repo"
}

# Install Python dependencies
install_python_deps() {
    echo -e "${BLUE}🐍 Setting up Python dependencies...${NC}"
    
    if ! command_exists python3; then
        echo -e "${RED}❌ Python 3 is required but not installed${NC}"
        exit 1
    fi
    
    # Check if pip is available
    if ! command_exists pip3 && ! python3 -m pip --version >/dev/null 2>&1; then
        echo -e "${RED}❌ pip is required but not available${NC}"
        exit 1
    fi
    
    # Install required packages
    local packages=("markdown" "pyyaml" "requests")
    for package in "${packages[@]}"; do
        log "Installing Python package: $package"
        python3 -m pip install --user "$package" || {
            echo -e "${YELLOW}⚠️  Failed to install $package, trying with pip3...${NC}"
            pip3 install --user "$package"
        }
    done
    
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
}

# Create configuration file
create_config() {
    local repo="$1"
    local config_file="$SCRIPT_DIR/.github-automation-config"
    
    cat > "$config_file" << EOF
# GitHub Issue Automation Configuration
# Generated on $(date)

# Repository settings
GITHUB_REPO="$repo"
GITHUB_USER="$(gh api user --jq .login)"

# File paths
CONSOLIDATED_ISSUES_FILE="$SCRIPT_DIR/.github/issues/consolidated-issues.md"
ISSUE_PARSER_SCRIPT="$SCRIPT_DIR/parse-issues.py"
ISSUE_CREATOR_SCRIPT="$SCRIPT_DIR/create-issues.sh"

# Default settings
DEFAULT_ASSIGNEE="@me"
RATE_LIMIT_DELAY=1
MAX_RETRIES=3
BATCH_SIZE=10

# Logging
LOG_LEVEL="INFO"
LOG_FILE="$SCRIPT_DIR/issue-automation.log"

# Advanced features
ENABLE_PROJECT_FIELDS=true
ENABLE_DEPENDENCY_TRACKING=true
DRY_RUN_MODE=false
EOF
    
    echo -e "${GREEN}✅ Configuration saved to: $config_file${NC}"
    log "Configuration file created: $config_file"
}

# Main setup function
main() {
    local repository=""
    local skip_install=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --repo)
                repository="$2"
                shift 2
                ;;
            --skip-install)
                skip_install=true
                shift
                ;;
            -h|--help)
                cat << EOF
GitHub Issue Automation - Setup Script

Usage: $0 [OPTIONS]

Options:
  --repo OWNER/REPO    Specify GitHub repository
  --skip-install       Skip GitHub CLI installation
  -h, --help          Show this help message

Examples:
  $0                                    # Interactive setup
  $0 --repo user/my-thesis-project    # Setup for specific repo
  $0 --skip-install                   # Skip CLI installation

EOF
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Unknown option: $1${NC}"
                exit 1
                ;;
        esac
    done
    
    echo -e "${PURPLE}🚀 GitHub Issue Automation Setup${NC}"
    echo "=================================="
    echo ""
    
    log "Starting GitHub Issue Automation setup"
    
    # Check if GitHub CLI is installed
    if command_exists gh; then
        echo -e "${GREEN}✅ GitHub CLI found${NC}"
        local gh_version=$(gh --version | head -1)
        log "GitHub CLI version: $gh_version"
    else
        if [[ "$skip_install" == true ]]; then
            echo -e "${RED}❌ GitHub CLI not found and --skip-install specified${NC}"
            exit 1
        else
            install_gh_cli
        fi
    fi
    
    # Check authentication
    if ! check_auth; then
        authenticate_github
    fi
    
    # Validate repository access
    validate_repository "$repository"
    local repo_name=$(cat "$SCRIPT_DIR/.repository")
    
    # Check repository features
    check_repository_features "$repo_name"
    
    # Install Python dependencies
    install_python_deps
    
    # Create configuration
    create_config "$repo_name"
    
    echo ""
    echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review your consolidated-issues.md file"
    echo "2. Run: ./create-issues.sh --preview (to preview issues)"
    echo "3. Run: ./create-issues.sh (to create issues)"
    echo ""
    echo -e "${CYAN}📁 Files created:${NC}"
    echo "  - $SCRIPT_DIR/.repository"
    echo "  - $SCRIPT_DIR/.github-automation-config"
    echo "  - $LOG_FILE"
    echo ""
    
    log "Setup completed successfully for repository: $repo_name"
}

# Run main function
main "$@"
