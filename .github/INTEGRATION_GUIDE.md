# Integration Guide: Smart Commits + Issue Management

This document explains how to integrate the enhanced AI smart commit system with the new issue management system for optimal workflow efficiency.

## Overview

The OPIT RAI9001 project now includes two powerful automation systems:

1. **AI Smart Commit System** (`ai-smart-commit.sh`) - Generates technically precise commit messages
2. **Issue Management System** (`add-issue.sh`) - Manages GitHub issues as markdown files

## Integrated Workflow

### 1. Issue-Driven Development

Start every feature or bug fix by creating an issue:

```bash
# Create a new issue
./add-issue.sh create "Implement data preprocessing pipeline" feature high

# This creates issue #017, work on it
git checkout -b issue-017-data-preprocessing
```

### 2. Development with Smart Commits

As you work on the issue, use the enhanced commit system:

```bash
# Stage your changes
git add src/data_preprocessing.py

# Use smart commit with issue reference
./ai-smart-commit.sh -f -p -m "Addresses #017: Add data preprocessing pipeline"

# Or let AI generate the message and add issue reference manually
./ai-smart-commit.sh -f -p
# Generated: "feat(data): implement pandas-based data cleaning pipeline"
# You can edit to: "feat(data): implement pandas-based data cleaning pipeline (#017)"
```

### 3. Issue Status Updates

Update issue status as you progress:

```bash
# Start working
./add-issue.sh status 17 in-progress

# Ready for review
./add-issue.sh status 17 review

# Complete
./add-issue.sh status 17 closed
```

## Enhanced Commit Message Patterns

The smart commit system now recognizes research-specific patterns:

### Data Analysis Commits
```bash
# Before: "update analysis"
# Enhanced: "feat(analysis): add statistical significance testing for experimental results"
```

### Research Documentation
```bash
# Before: "update docs"  
# Enhanced: "docs(thesis): add methodology section with experimental design details"
```

### Algorithm Implementation
```bash
# Before: "fix bug"
# Enhanced: "fix(algorithm): resolve off-by-one error in neural network layer indexing"
```

### LaTeX/Thesis Changes
```bash
# Before: "thesis update"
# Enhanced: "docs(thesis): update literature review with 15 new references from 2024"
```

## Commit Message + Issue Integration Examples

### Feature Development
```bash
# Create issue
./add-issue.sh create "Implement neural network evaluation metrics" feature high
# Created issue #018

# Work and commit
git add src/evaluation/metrics.py
./ai-smart-commit.sh -f -p -m "feat(eval): implement accuracy and F1-score metrics for neural networks

Implements core evaluation metrics requested in #018:
- Accuracy calculation with confusion matrix
- F1-score with precision/recall breakdown  
- Support for multi-class classification
- Batch processing optimization

Closes #018"
```

### Bug Fix
```bash
# Create bug report
./add-issue.sh create "Fix memory leak in data loader" bug critical
# Created issue #019

# Fix and commit
git add src/data/loader.py
./ai-smart-commit.sh -f -p -m "fix(data): resolve memory leak in batch data loader

Fixes #019 by properly closing file handles and clearing
cache after each batch. Memory usage reduced by 80%.

- Add explicit file handle cleanup
- Clear tensor cache between batches
- Add memory usage monitoring"
```

### Research Analysis
```bash
# Create analysis task
./add-issue.sh create "Statistical analysis of experimental results" analysis medium
# Created issue #020

# Analyze and commit
git add notebooks/statistical_analysis.ipynb
./ai-smart-commit.sh -f -p -m "analysis: complete statistical significance testing for model comparison

Addresses #020 with comprehensive statistical analysis:
- ANOVA testing across 5 model variants
- Post-hoc Tukey HSD comparisons  
- Effect size calculations (Cohen's d)
- Confidence intervals for performance metrics

Results show significant improvement (p < 0.001) for proposed method."
```

## Advanced Integration Techniques

### 1. Automated Issue Creation from Commits

You can create issues directly from commit analysis:

```bash
# If smart commit detects a TODO or FIXME
./ai-smart-commit.sh -f -p
# Generated: "refactor(core): optimize algorithm performance TODO: investigate memory usage"

# Automatically create follow-up issue
./add-issue.sh create "Investigate memory usage in core algorithm" enhancement medium
```

### 2. Issue Reference Automation

Create aliases for common patterns:

```bash
# Add to .smart-commit-aliases
alias sci='./ai-smart-commit.sh -f -p'  # Smart commit interactive
alias scf='./ai-smart-commit.sh -f'     # Smart commit fast
alias issue='./add-issue.sh'            # Issue management

# Workflow becomes:
issue create "New feature" feature high  # Creates #021
git checkout -b issue-021-new-feature
# ... work ...
sci -m "feat: implement new feature (#021)"
issue status 21 closed
```

### 3. Branch Naming Integration

Update your git workflow to use issue numbers:

```bash
# Function to add to your shell profile
work_on_issue() {
    local issue_num=$1
    local description=$(./add-issue.sh list | grep "#$(printf "%03d" $issue_num)" | sed 's/.*] //')
    local branch_name="issue-$(printf "%03d" $issue_num)-$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')"
    
    git checkout -b "$branch_name"
    ./add-issue.sh status $issue_num in-progress
    echo "Working on issue #$issue_num: $description"
}

# Usage:
work_on_issue 22  # Creates branch and updates status
```

## Commit Message Templates

### Research Project Templates

The smart commit system now includes research-specific templates:

```bash
# Thesis/Documentation
docs(thesis): [action] [section] [details]
docs(proposal): [action] [details]  
docs(progress): [action] [milestone/meeting] [details]

# Research Analysis
analysis: [type] analysis [of what] [results summary]
research: [methodology/experiment] [brief description]

# Data Management  
data: [action] [dataset/source] [processing details]
feat(data): [new capability] [for what purpose]

# Algorithm/Model Changes
feat(model): [new algorithm/improvement] [performance impact]
fix(algorithm): [specific fix] [in which component]
perf(model): [optimization] [performance improvement]

# Evaluation/Testing
test: [add/update] [type] tests [for component]
eval: [metric/benchmark] [results summary]
```

### Issue Reference Patterns

Standardize how you reference issues:

```bash
# Addressing an issue (work in progress)
"feat(data): implement data validation pipeline (#015)"

# Fixing a bug (resolves the issue)  
"fix(parser): handle malformed JSON input

Fixes #023 by adding try-catch blocks and validation"

# Related to multiple issues
"refactor(core): optimize memory usage (#018, #019)

Related to #020 - performance analysis"

# Partial progress
"feat(analysis): add preliminary statistical tests

Addresses part of #025 - full implementation in next commit"
```

## Workflow Automation Scripts

### Daily Research Workflow

Create a script for common daily tasks:

```bash
#!/bin/bash
# daily-research.sh

echo "🔬 Daily Research Workflow"
echo "=========================="

# Show open issues
echo "📋 Open Issues:"
./add-issue.sh list open

# Show recent commits
echo -e "\n📝 Recent Commits:"
git log --oneline -5

# Show current branch status
echo -e "\n🌿 Current Branch:"
git status --porcelain

# Offer to create new issue
read -p "Create new issue? (y/N): " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n"
    read -p "Issue title: " title
    read -p "Type [feature]: " type
    read -p "Priority [medium]: " priority
    ./add-issue.sh create "$title" "${type:-feature}" "${priority:-medium}"
fi
```

### End-of-Day Commit Summary

```bash
#!/bin/bash
# eod-summary.sh

echo "📊 End of Day Summary"
echo "===================="

# Show today's commits
echo "📝 Today's Commits:"
git log --since="1 day ago" --oneline --author="$(git config user.name)"

# Show updated issues
echo -e "\n📋 Updated Issues Today:"
find .github/issues -name "issue-*.md" -mtime -1 -exec basename {} \; | sort

# Suggest status updates
echo -e "\n🔄 Issues to Update:"
./add-issue.sh list in-progress
```

## Best Practices Summary

### Commit Best Practices
1. **Use the AI system**: Let it generate technically precise messages
2. **Add issue references**: Link commits to issues for traceability  
3. **Be specific**: Technical details make better commit history
4. **Include impact**: Mention performance improvements or fixes

### Issue Management Best Practices
1. **Start with issues**: Create issues before starting work
2. **Update status regularly**: Keep issue status current
3. **Use descriptive titles**: Make issues easy to search and understand
4. **Link related work**: Reference related issues and commits

### Integration Best Practices
1. **Consistent naming**: Use issue numbers in branch names
2. **Regular synchronization**: Keep issues and commits in sync
3. **Document decisions**: Use issues to record research decisions
4. **Automate workflows**: Use scripts to reduce manual overhead

This integrated system provides a powerful foundation for managing complex research projects with clear traceability from issues through implementation to completion.
