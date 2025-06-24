# thiLLMo Smart Commit System

🤖 **AI-Enhanced Git Workflow with Automatic Prompt Logging**

An intelligent commit system that automates git workflows while capturing AI assistant interactions, prompts, and context for better development tracking and reproducibility.

## 🌟 Features

- **🤖 AI-Powered Suggestions**: Automatically analyzes changes and suggests appropriate commit types and messages
- **📊 Intelligent Analysis**: Categorizes file changes and detects patterns
- **🔍 Auto-Detection**: Smart commit type detection based on file patterns and change types
- **📝 Prompt Logging**: Captures AI assistant usage, prompts, and context in commit messages
- **🚀 Smart Push**: Intelligent remote push with branch detection and error handling
- **📚 History Tracking**: Maintains a history of commits with timestamps
- **⚙️ Configurable**: Customizable defaults and behavior
- **🎯 Project-Aware**: Special handling for thiLLMo project patterns (ontology, OG-RAG, proverbs)

## 🚀 Quick Start

### 1. Setup
```bash
./setup-smart-commit.sh
```

### 2. Basic Usage
```bash
# Interactive AI-enhanced commit
./ai-smart-commit.sh

# Quick commit all changes
./ai-smart-commit.sh --quick

# Quick commit and push
./ai-smart-commit.sh --quick --push
```

### 3. With Aliases (after setup)
```bash
aic          # AI-enhanced interactive commit
qc           # Quick commit
qcp          # Quick commit and push
```

## 📋 Available Scripts

### `ai-smart-commit.sh` (Recommended)
The main AI-enhanced commit script with full analysis and suggestions.

**Options:**
- `-q, --quick` - Quick mode (auto-stage all, minimal prompts)
- `-a, --all` - Stage all changes automatically
- `-p, --push` - Auto-push after successful commit
- `-v, --verbose` - Verbose output (default)
- `-s, --silent` - Minimal output
- `-c, --config` - Show current configuration
- `--history` - Show recent commit history

### `smart-commit.sh`
Simpler version with basic smart features.

### `setup-smart-commit.sh`
One-time setup script for configuration and aliases.

## 🧠 How It Works

### 1. **Change Analysis**
```
📊 Analyzing your staged files:
- File types (code, docs, config, tests)
- Change types (new, modified, deleted)
- Project-specific patterns
```

### 2. **Smart Suggestions**
```
💡 Based on analysis:
- Suggests appropriate commit type (feat, fix, docs, etc.)
- Generates context-aware commit messages
- Provides multiple options to choose from
```

### 3. **AI Context Capture**
```
🤖 Automatically logs:
- AI Assistant used (GitHub Copilot, ChatGPT, etc.)
- Model information (GPT-4, Claude, etc.)
- Original prompts and context
- Session information
```

### 4. **Commit Integration**
```
🔗 Integrates with existing commitizen config:
- Uses your .cz.toml configuration
- Maintains conventional commit format
- Adds AI context as structured metadata
```

## ⚙️ Configuration

### Default Configuration File (`.smart-commit-config`)
```bash
# thiLLMo Smart Commit Configuration
DEFAULT_ASSISTANT="GitHub Copilot"
DEFAULT_MODEL="GPT-4"
AUTO_PUSH=false
QUICK_MODE=false
VERBOSE=true
SAVE_HISTORY=true
```

### Commitizen Integration
The system works with your existing `.cz.toml` configuration:

```toml
[tool.commitizen.customize]
message_template = """{{change_type}}{{scope}}: {{subject}}

{{body}}

{% if prompt %}
Prompt: {{prompt}}
{% endif %}
{% if prompt_context %}
Prompt-context: {{prompt_context}}
{% endif %}
{% if ai_assistant %}
AI-assistant: {{ai_assistant}}
{% endif %}
{% if ai_model %}
AI-model: {{ai_model}}
{% endif %}
{{footer}}"""
```

## 🎯 Project-Specific Intelligence

### thiLLMo-Aware Suggestions

**Ontology Changes:**
- `feat: enhance cultural ontology structure`
- `feat: add new ontology components`

**OG-RAG System:**
- `feat: improve OG-RAG system implementation`
- `fix: resolve OG-RAG pipeline issues`

**Proverb Processing:**
- `feat: add Kikuyu proverb processing`
- `docs: document proverb translation methodology`

## 📝 Example Workflow

### Interactive Mode
```bash
$ ./ai-smart-commit.sh

🎯 thiLLMo AI-Enhanced Smart Commit

📋 Current repository status:
M  src/ontology/cultural_concepts.py
A  docs/thesis/chapters/03-methodology.tex
M  README.md

Stage all changes? (Y/n): y
📁 All changes staged

🔍 Analyzing changes...
📊 Change Analysis: 3 files, 1 new, 2 modified

📁 File Changes:
 docs/thesis/chapters/03-methodology.tex | 45 +++++++++
 src/ontology/cultural_concepts.py      | 12 ++-
 README.md                              |  8 +-
 3 files changed, 63 insertions(+), 2 deletions(-)

💡 Smart suggestions:
   1. feat: enhance cultural ontology structure
   2. docs: add methodology documentation
   3. feat: implement new ontology components

🤖 AI-powered commit message suggestions
🚀 Launching commitizen with AI context...

? Select the type of change you are committing: feat
? Scope (optional): ontology
? Subject: enhance cultural ontology with methodology docs
? Body (optional): 
Add detailed methodology documentation and improve cultural concept definitions in the ontology system.
? Actual prompt used (optional): Create a comprehensive smart commit system that automates git workflow
? Prompt context (optional): Working on thiLLMo project structure and development tools
? AI Assistant used (optional): GitHub Copilot
? AI Model used (optional): GPT-4
? Footer (optional): 

✅ Commit created successfully!

📤 Push changes to remote?
   Current branch: dev
   Remote: origin

Push now? (Y/n): y
🚀 Pushing to origin/dev...
✅ Changes pushed successfully!
🔗 Remote URL: git@github.com:username/opit-rai9001.git

🎉 Smart commit completed successfully!
```

### Quick Mode
```bash
$ ./ai-smart-commit.sh --quick --push

🎯 thiLLMo AI-Enhanced Smart Commit
📁 All changes staged automatically
🔍 Analyzing changes...
🔄 Auto-pushing changes...
✅ Changes pushed successfully!
🎉 Smart commit completed successfully!
```

## 🔍 Viewing History and Configuration

```bash
# Show recent commits
./ai-smart-commit.sh --history

# Show current configuration
./ai-smart-commit.sh --config

# Show help
./ai-smart-commit.sh --help
```

## 🛠️ Troubleshooting

### Common Issues

**Commitizen not found:**
```bash
pip install commitizen
# or
npm install -g commitizen
```

**Permission denied:**
```bash
chmod +x *.sh
```

**Git user not configured:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Debugging
Run with verbose mode to see detailed output:
```bash
./ai-smart-commit.sh --verbose
```

## 🤝 Integration with Development Workflow

### VS Code Integration
The script works seamlessly with VS Code and GitHub Copilot, automatically detecting recent AI interactions.

### Git Hooks
You can integrate this as a git hook for automatic AI context capture:

```bash
# In .git/hooks/prepare-commit-msg
#!/bin/sh
./ai-smart-commit.sh --quick
```

### CI/CD Integration
The commit format with AI context is perfect for automated analysis and documentation generation.

## 📊 Commit Message Format

Example generated commit:
```
feat(ontology): enhance cultural ontology with methodology docs

Add detailed methodology documentation and improve cultural concept 
definitions in the ontology system.

Prompt: Create a comprehensive smart commit system that automates git workflow
Prompt-context: Working on thiLLMo project structure and development tools  
AI-assistant: GitHub Copilot
AI-model: GPT-4
```

## 🚀 Advanced Usage

### Custom AI Context
You can manually specify AI context:
```bash
export AI_ASSISTANT="Claude"
export AI_MODEL="Claude-3"
export AI_PROMPT="Your custom prompt here"
./ai-smart-commit.sh
```

### Batch Commits
For multiple commits with similar context:
```bash
./ai-smart-commit.sh --config > /tmp/ai-context
# Multiple commits will reuse this context
```

## 📚 Best Practices

1. **Use descriptive prompts**: The more context you provide, the better the commit history
2. **Review suggestions**: While AI suggestions are smart, always review before committing
3. **Maintain consistency**: Use the same assistant/model info for related work
4. **Regular configuration updates**: Keep your `.smart-commit-config` file updated
5. **History review**: Regularly check `--history` to track your development patterns

## 🔮 Future Enhancements

- **Browser Integration**: Detect ChatGPT/Claude usage in browser
- **VS Code Extension**: Direct integration with VS Code
- **Prompt Template Library**: Pre-defined prompts for common tasks
- **AI Model Comparison**: Track which models work best for different tasks
- **Automated Documentation**: Generate docs from commit AI context
- **Team Collaboration**: Share AI context across team members

## 📄 License

Part of the thiLLMo project - Culturally Faithful Kikuyu Proverb Translation system.
