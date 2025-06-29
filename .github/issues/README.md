# Issue Management System - OPIT RAI9001

This directory contains a comprehensive issue management system for tracking GitHub issues as markdown files in the local repository.

## Directory Structure

```
.github/issues/
├── README.md                 # This file
├── consolidated-issues.md    # Master list of all project issues
├── issue-template.md         # Template for new issues
├── issue-001-*.md           # Individual issue files
├── issue-002-*.md
└── ...
```

## Quick Start

### 1. List All Issues
```bash
./add-issue.sh list
```

### 2. Create a New Issue

**Interactive Mode (Recommended):**
```bash
./add-issue.sh create
```
This will prompt you for all issue fields including:
- Title (required)
- Labels (types, priority, status, etc.)
- Assignee (defaults to @me)
- Due date (optional, YYYY-MM-DD format)
- Issue description (multi-line, end with 'END')
- Project fields (sprint, criticality, deadlines, etc.)

**Quick Mode:**
```bash
./add-issue.sh create "Issue Title"
```
Prompts for additional fields after providing the title.

**Legacy Mode:**
```bash
./add-issue.sh create "Fix data preprocessing bug" bug high @assignee
```
Uses the old format for backward compatibility.

### 3. Extract Issue from Consolidated File
```bash
./add-issue.sh extract 5
```

### 4. Update Issue Status
```bash
./add-issue.sh status 3 in-progress
```

### 5. Search Issues
```bash
./add-issue.sh search "algorithm"
```

## Issue Management Workflow

### Creating New Issues

1. **Use Interactive Mode** (recommended for complete issue setup):
   ```bash
   ./add-issue.sh create
   ```
   
   The script will guide you through:
   - **Title**: Required issue title
   - **Labels**: Comma-separated labels (feature, bug, critical, high, week-1, etc.)
   - **Assignee**: GitHub username (defaults to @me)
   - **Due Date**: Optional deadline in YYYY-MM-DD format
   - **Description**: Multi-line issue body (type 'END' on new line to finish)
   - **Project Fields**: Optional fields including:
     - Sprint/Week (e.g., "Week 1 (Jun 20-26)")
     - Criticality (🚨 CRITICAL, 🛑 BLOCKER, ⚠️ HIGH, 📋 MEDIUM, 💡 LOW)
     - OPIT Deadline (e.g., "Examining Committee (Jul 13)")
     - Thesis Section (e.g., "Introduction", "Methodology")
     - Effort Hours (estimated hours)

2. **Issues follow consolidated-issues.md format** for consistency:
   - **TITLE**: Issue title
   - **LABELS**: Comma-separated tags
   - **ASSIGNEE**: GitHub username with @
   - **DUE_DATE**: Optional deadline
   - **BODY**: Detailed description in code block
   - **PROJECT_FIELDS**: Optional project-specific metadata
   ```

2. **Manual creation** from template:
   ```bash
   ./add-issue.sh template  # View template
   cp .github/issues/issue-template.md .github/issues/issue-XXX-title.md
   ```

3. **Extract from consolidated file**:
   ```bash
   ./add-issue.sh extract 12
   ```

### Issue Types
- **bug**: Something that's broken and needs fixing
- **feature**: New functionality or capability
- **enhancement**: Improvement to existing functionality
- **documentation**: Documentation updates or additions
- **research**: Research tasks and investigations
- **analysis**: Data analysis and evaluation tasks

### Priority Levels
- **critical**: Blocking progress, immediate attention required
- **high**: Important for project success, high priority
- **medium**: Useful improvements, moderate priority
- **low**: Nice-to-have features, low priority

### Status Workflow
1. **open**: Issue identified, ready for work
2. **in-progress**: Actively being worked on
3. **review**: Completed, pending review/testing
4. **closed**: Completed and verified

## File Naming Convention

Individual issue files follow this naming pattern:
```
issue-XXX-descriptive-title.md
```

Where:
- `XXX` is a zero-padded 3-digit issue number (001, 002, etc.)
- `descriptive-title` is a URL-friendly version of the issue title

Examples:
- `issue-001-literature-review-analysis.md`
- `issue-012-fix-data-preprocessing-bug.md`
- `issue-025-implement-evaluation-metrics.md`

## Issue Template Structure

Each issue follows a standardized template with these sections:

### Header Information
- **Type**: Classification of the issue
- **Priority**: Urgency level
- **Status**: Current state
- **Assignee**: Person responsible
- **Labels**: Tags for categorization
- **Created/Updated**: Timestamps

### Content Sections
- **Description**: Detailed explanation
- **Acceptance Criteria**: Definition of done
- **Technical Details**: Implementation notes
- **Related Issues**: Dependencies and relationships
- **Files/Components Affected**: Code areas involved
- **Notes**: Additional information
- **Progress Log**: Chronological updates

## Enhanced Issue Format

The system now supports the consolidated-issues.md format with these fields:

### Required Fields
- **TITLE**: Issue title (same as markdown header)
- **LABELS**: Comma-separated tags (e.g., "feature,high,week-1")
- **ASSIGNEE**: GitHub username with @ prefix

### Optional Fields
- **DUE_DATE**: Deadline in YYYY-MM-DD format
- **BODY**: Multi-line description in markdown code block
- **PROJECT_FIELDS**: Project-specific metadata including:
  - `Sprint_Week`: Sprint or week identifier
  - `Criticality`: Visual priority indicator (🚨🛑⚠️📋💡)
  - `OPIT_Deadline`: Academic milestone deadlines
  - `Thesis_Section`: Related thesis chapter/section
  - `Effort_Hours`: Estimated time investment

### Example Format
```markdown
# Issue #015: Test Interactive Issue

**TITLE:** Test Interactive Issue
**LABELS:** feature,test,medium
**ASSIGNEE:** @test-user
**DUE_DATE:** 2025-07-01
**BODY:**
\```
This is a test issue description
for testing the new interactive prompts.
\```

**PROJECT_FIELDS:**
- Sprint_Week: Week 1 Test
- Criticality: 📋 MEDIUM
- OPIT_Deadline: Test Deadline
- Thesis_Section: Testing
- Effort_Hours: 2
```

## Advanced Usage

### Filtering Issues by Status
```bash
./add-issue.sh list open          # Only open issues
./add-issue.sh list in-progress   # Only in-progress issues
./add-issue.sh list closed        # Only closed issues
```

### Searching by Keywords
```bash
./add-issue.sh search "algorithm"     # Find algorithm-related issues
./add-issue.sh search "documentation" # Find documentation issues
./add-issue.sh search "bug"          # Find bug reports
```

### Batch Operations

To update multiple issues, you can use shell loops:
```bash
# Mark multiple issues as closed
for issue in 5 7 12; do
    ./add-issue.sh status $issue closed
done
```

## Integration with Git Workflow

### Commit Message Integration
When working on issues, reference them in commit messages:
```bash
git commit -m "fix: resolve data preprocessing bug

Fixes #005 by implementing proper null handling in the
data cleaning pipeline.

- Add null value detection
- Implement fallback strategies
- Update unit tests"
```

### Branch Naming
Create branches that reference issue numbers:
```bash
git checkout -b issue-005-fix-data-preprocessing
git checkout -b feature/issue-012-evaluation-metrics
```

## Maintenance Tasks

### Regular Maintenance
1. **Weekly**: Update issue statuses and progress logs
2. **Monthly**: Review closed issues and archive if needed
3. **Before milestones**: Ensure all related issues are updated

### Synchronization
If using GitHub Issues alongside this system:
1. Keep issue numbers synchronized
2. Cross-reference GitHub issue numbers in markdown files
3. Use GitHub's API to sync status updates if needed

## Tips and Best Practices

### Writing Good Issue Descriptions
- Be specific and actionable
- Include context and background
- Define clear acceptance criteria
- Reference related work or dependencies

### Using Labels Effectively
- Combine multiple labels for better filtering
- Use consistent labeling conventions
- Include component/module labels for large projects

### Managing Dependencies
- Use "Blocks" and "Blocked by" relationships
- Create dependency graphs for complex features
- Plan issue order based on dependencies

### Progress Tracking
- Update progress logs regularly
- Include specific achievements and blockers
- Document decisions and rationale changes

## Troubleshooting

### Script Issues
If the `add-issue.sh` script doesn't work:
1. Check execute permissions: `chmod +x add-issue.sh`
2. Ensure you're in the project root directory
3. Verify bash is available in your PATH

### File Conflicts
If issue numbers conflict:
1. Check both individual files and consolidated file
2. Use `get_next_issue_number()` function logic
3. Manually resolve conflicts by renumbering

### Template Updates
To update the issue template:
1. Modify `issue-template.md`
2. Update the script's template creation function
3. Apply changes to new issues going forward

## Automation Opportunities

Future enhancements could include:
- GitHub Actions integration for issue sync
- Automated status updates based on commit messages
- Issue metrics and reporting dashboards
- Integration with project management tools
- Automated deadline and milestone tracking

## Support

For questions or issues with the issue management system:
1. Check this README for common solutions
2. Review the `add-issue.sh` script source code
3. Create a new issue using the system itself
4. Document any improvements or bug fixes
