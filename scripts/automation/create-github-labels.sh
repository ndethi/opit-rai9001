#!/bin/bash

# Create GitHub labels for the thesis project
# This script creates all the labels used in consolidated-issues.md

set -e

echo "🏷️  Creating GitHub labels for thesis project..."

# Color scheme for different types of labels
PLANNING_COLOR="1d76db"      # Blue
SPRINT_COLOR="0e8a16"        # Green  
WEEK_COLOR="f9d0c4"          # Light peach
PRIORITY_COLOR="d93f0b"      # Red
MILESTONE_COLOR="5319e7"     # Purple
ADMIN_COLOR="fbca04"         # Yellow
INFRASTRUCTURE_COLOR="c2e0c6" # Light green
DEADLINE_COLOR="b60205"      # Dark red

# Function to create label if it doesn't exist
create_label() {
    local name="$1"
    local description="$2"
    local color="$3"
    
    echo "Creating label: $name"
    
    # Check if label exists
    if gh label list --json name -q ".[].name" | grep -q "^$name$"; then
        echo "  ✅ Label '$name' already exists"
    else
        if gh label create "$name" --description "$description" --color "$color"; then
            echo "  ✅ Created label '$name'"
        else
            echo "  ❌ Failed to create label '$name'"
        fi
    fi
}

echo ""
echo "Creating planning and sprint labels..."
create_label "planning" "Project planning and coordination tasks" "$PLANNING_COLOR"
create_label "sprint" "Sprint-related tasks and milestones" "$SPRINT_COLOR"

echo ""
echo "Creating week labels..."
for week in {1..10}; do
    create_label "week-$week" "Tasks for week $week of the project" "$WEEK_COLOR"
done

echo ""
echo "Creating priority labels..."
create_label "critical" "Critical priority - must complete on time" "$PRIORITY_COLOR"
create_label "high" "High priority - important for project success" "d93f0b"
create_label "blocker" "Blocking other tasks - immediate attention required" "b60205"
create_label "urgent" "Urgent - needs immediate action" "d93f0b"

echo ""
echo "Creating milestone and deadline labels..."
create_label "milestone" "Project milestone or deliverable" "$MILESTONE_COLOR"
create_label "critical-deadline" "Critical deadline - cannot be missed" "$DEADLINE_COLOR"
create_label "july-13-deadline" "Tasks due by July 13 deadline" "$DEADLINE_COLOR"
create_label "july-13" "July 13 deadline related" "$DEADLINE_COLOR"
create_label "july-27-deadline" "Tasks due by July 27 deadline" "$DEADLINE_COLOR"
create_label "july-27" "July 27 deadline related" "$DEADLINE_COLOR"
create_label "august-3" "August 3 deadline related" "$DEADLINE_COLOR"
create_label "august-30" "August 30 final deadline related" "$DEADLINE_COLOR"
create_label "final-deadline" "Final project deadline" "$DEADLINE_COLOR"
create_label "defense-form-deadline" "Defense form submission deadline" "$DEADLINE_COLOR"

echo ""
echo "Creating category labels..."
create_label "admin" "Administrative tasks and paperwork" "$ADMIN_COLOR"
create_label "infrastructure" "Technical infrastructure and setup" "$INFRASTRUCTURE_COLOR"
create_label "setup" "Initial setup and configuration tasks" "$INFRASTRUCTURE_COLOR"
create_label "meeting" "Meetings and appointments" "c5def5"
create_label "supervisor" "Supervisor meetings and feedback" "c5def5"
create_label "proposal" "Research proposal related tasks" "0075ca"
create_label "diagrams" "Diagram creation and visualization" "0075ca"
create_label "data-collection" "Data collection and sourcing" "a2eeef"
create_label "methodology" "Research methodology tasks" "a2eeef"
create_label "thesis-draft" "Thesis writing and drafting" "7057ff"
create_label "implementation" "System implementation tasks" "0e8a16"
create_label "evaluation" "Evaluation and testing tasks" "fbca04"
create_label "defense" "Defense preparation and presentation" "5319e7"

echo ""
echo "🎉 Label creation complete!"
echo ""
echo "📋 Verifying created labels..."
gh label list | head -20
