#!/bin/bash

# Week 1 Issue Creator - Final Version
set -e

# Disable GitHub CLI pager
export GH_PAGER=""
export PAGER=""

echo "🎯 Creating Week 1 Issues - Final Attempt"
echo "========================================"

# Create issues manually with proper data
echo ""
echo "📝 Creating WEEK_1_SPRINT issue..."

gh issue create \
  --title "[SPRINT W1] Week 1 Planning - Foundation Sprint" \
  --body "Week 1 Sprint: Foundation & Proposal Enhancement. Complete project infrastructure setup and enhance research proposal with OG-RAG architecture diagrams per supervisor feedback." \
  --label "planning,sprint,week-1,critical" \
  --assignee "ndethi"

echo "✅ Created WEEK_1_SPRINT"
sleep 2

echo ""
echo "📝 Creating WEEK_1_TASK_1 issue..."

gh issue create \
  --title "[BLOCKER] Verify Partnership Agreement Status - URGENT" \
  --body "Verify partnership agreement status immediately. This is blocking project start and needs urgent attention." \
  --label "blocker,urgent,admin,week-1" \
  --assignee "ndethi"

echo "✅ Created WEEK_1_TASK_1"
sleep 2

echo ""
echo "📝 Creating WEEK_1_TASK_2 issue..."

gh issue create \
  --title "[CRITICAL] Add OG-RAG Architecture Diagrams to Research Proposal" \
  --body "Add OG-RAG architecture diagrams to the research proposal as requested by supervisor. This is critical for project approval." \
  --label "critical,proposal,diagrams,week-1" \
  --assignee "ndethi"

echo "✅ Created WEEK_1_TASK_2"
sleep 2

echo ""
echo "📝 Creating WEEK_1_TASK_3 issue..."

gh issue create \
  --title "[CRITICAL] Complete GitHub Project and LaTeX Infrastructure Setup" \
  --body "Complete GitHub repository setup and LaTeX infrastructure for thesis writing. This includes project management tools and development environment." \
  --label "critical,infrastructure,setup,week-1" \
  --assignee "ndethi"

echo "✅ Created WEEK_1_TASK_3"
sleep 2

echo ""
echo "📝 Creating WEEK_1_MEETING issue..."

gh issue create \
  --title "[MEETING] Supervisor Meeting #1 - Project Kickoff & Enhanced Proposal" \
  --body "First supervisor meeting to discuss project kickoff and review the enhanced proposal with OG-RAG architecture diagrams." \
  --label "meeting,supervisor,week-1" \
  --assignee "ndethi"

echo "✅ Created WEEK_1_MEETING"

echo ""
echo "🎉 All Week 1 issues created successfully!"
echo ""
echo "📋 Current issues in repository:"
gh issue list --limit 10 --json number,title,labels --jq '.[] | "\(.number): \(.title) [\(.labels | map(.name) | join(","))]"'
