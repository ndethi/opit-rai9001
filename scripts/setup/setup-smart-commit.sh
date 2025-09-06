#!/bin/bash

# thiLLMo Smart Commit Setup Script
# Configures the smart commit tools and aliases

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 thiLLMo Smart Commit Setup${NC}"
echo

# Check if we're in the right directory
if [ ! -f "ai-smart-commit.sh" ] || [ ! -f ".cz.toml" ]; then
    echo -e "${RED}❌ Error: Run this script from the project root directory${NC}"
    echo "   Expected files: ai-smart-commit.sh, .cz.toml"
    exit 1
fi

# Make scripts executable
echo -e "${BLUE}🔧 Making scripts executable...${NC}"
chmod +x smart-commit.sh
chmod +x ai-smart-commit.sh
echo -e "${GREEN}✅ Scripts are now executable${NC}"
echo

# Test commitizen installation
echo -e "${BLUE}🔍 Checking commitizen installation...${NC}"
if command -v cz &> /dev/null; then
    echo -e "${GREEN}✅ Commitizen is installed${NC}"
    cz version
else
    echo -e "${YELLOW}⚠️  Commitizen not found${NC}"
    echo "   Install with: pip install commitizen"
    echo "   Or: npm install -g commitizen"
fi
echo

# Check git configuration
echo -e "${BLUE}🔍 Checking git configuration...${NC}"
if git config user.name > /dev/null && git config user.email > /dev/null; then
    echo -e "${GREEN}✅ Git user configuration found${NC}"
    echo "   Name: $(git config user.name)"
    echo "   Email: $(git config user.email)"
else
    echo -e "${YELLOW}⚠️  Git user not configured${NC}"
    echo "   Run: git config --global user.name 'Your Name'"
    echo "   Run: git config --global user.email 'your.email@example.com'"
fi
echo

# Offer to install aliases
echo -e "${BLUE}💡 Install shell aliases for easy access?${NC}"
echo "   This will add aliases like 'aic' for ai-smart-commit"
read -p "   Install aliases? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Detect shell
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.bashrc"  # Default fallback
    fi
    
    echo -e "${BLUE}📝 Adding aliases to $SHELL_RC...${NC}"
    
    # Check if aliases are already installed
    if grep -q "thiLLMo Smart Commit Aliases" "$SHELL_RC" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Aliases already installed${NC}"
    else
        echo "" >> "$SHELL_RC"
        echo "# thiLLMo Smart Commit Aliases" >> "$SHELL_RC"
        echo "alias aic='cd $(pwd) && ./ai-smart-commit.sh'" >> "$SHELL_RC"
        echo "alias sc='cd $(pwd) && ./smart-commit.sh'" >> "$SHELL_RC"
        echo "alias qc='cd $(pwd) && ./ai-smart-commit.sh --quick'" >> "$SHELL_RC"
        echo "alias qcp='cd $(pwd) && ./ai-smart-commit.sh --quick --push'" >> "$SHELL_RC"
        
        echo -e "${GREEN}✅ Aliases installed to $SHELL_RC${NC}"
        echo -e "${BLUE}   Run 'source $SHELL_RC' to activate${NC}"
    fi
fi

echo

# Create initial configuration
echo -e "${BLUE}⚙️  Creating initial configuration...${NC}"
if [ ! -f ".smart-commit-config" ]; then
    cat > .smart-commit-config << EOF
# thiLLMo Smart Commit Configuration
DEFAULT_ASSISTANT="GitHub Copilot"
DEFAULT_MODEL="GPT-4"
AUTO_PUSH=false
QUICK_MODE=false
VERBOSE=true
SAVE_HISTORY=true
EOF
    echo -e "${GREEN}✅ Configuration file created${NC}"
else
    echo -e "${BLUE}ℹ️  Configuration file already exists${NC}"
fi

# Test the setup
echo
echo -e "${BLUE}🧪 Testing smart commit setup...${NC}"
echo "Running: ./ai-smart-commit.sh --help"
echo
./ai-smart-commit.sh --help

echo
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo
echo -e "${BLUE}📖 Usage Examples:${NC}"
echo "   ./ai-smart-commit.sh              # Interactive AI-enhanced commit"
echo "   ./ai-smart-commit.sh --quick      # Quick commit all changes"
echo "   ./ai-smart-commit.sh --quick --push   # Quick commit and push"
echo "   ./ai-smart-commit.sh --config     # Show configuration"
echo "   ./ai-smart-commit.sh --history    # Show commit history"
echo
echo -e "${BLUE}💡 Pro Tips:${NC}"
echo "   - The script automatically detects file types and suggests commit types"
echo "   - AI context (assistant, model, prompts) is logged with each commit"
echo "   - Use --quick mode for fast commits without prompts"
echo "   - Configuration is saved in .smart-commit-config"
echo
echo -e "${YELLOW}⚠️  Next Steps:${NC}"
if ! command -v cz &> /dev/null; then
    echo "   1. Install commitizen: pip install commitizen"
fi
echo "   2. Test with: ./ai-smart-commit.sh"
echo "   3. Customize .smart-commit-config as needed"
echo
