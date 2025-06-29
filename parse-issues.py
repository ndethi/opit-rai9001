#!/usr/bin/env python3

"""
GitHub Issue Parser
Parses consolidated-issues.md file and extracts issue data into JSON format
"""

import re
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IssueParser:
    def __init__(self, markdown_file: str):
        self.markdown_file = markdown_file
        self.issues = []
        
    def parse_markdown(self) -> List[Dict[str, Any]]:
        """Parse the markdown file and extract issue data"""
        try:
            with open(self.markdown_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            logger.info(f"Parsing markdown file: {self.markdown_file}")
            
            # Split content into issue sections
            # Look for patterns like ## ISSUE_ID or ## WEEK_X_SPRINT
            issue_sections = re.split(r'\n(?=##\s+\w)', content)
            
            for section in issue_sections:
                if not section.strip():
                    continue
                
                issue_data = self._parse_issue_section(section)
                if issue_data:
                    self.issues.append(issue_data)
            
            logger.info(f"Successfully parsed {len(self.issues)} issues")
            return self.issues
            
        except FileNotFoundError:
            logger.error(f"Markdown file not found: {self.markdown_file}")
            raise
        except Exception as e:
            logger.error(f"Error parsing markdown file: {e}")
            raise
    
    def _parse_issue_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Parse an individual issue section"""
        lines = section.strip().split('\n')
        if not lines:
            return None
        
        # Extract issue ID from header
        header_match = re.match(r'^##\s+(.+)$', lines[0])
        if not header_match:
            return None
        
        issue_id = header_match.group(1).strip()
        
        # Skip if this isn't an issue section (e.g., just a regular header)
        if not self._looks_like_issue_section(section):
            return None
        
        issue_data = {
            'id': issue_id,
            'title': '',
            'labels': [],
            'assignee': '',
            'due_date': '',
            'body': '',
            'project_fields': {},
            'raw_section': section
        }
        
        # Parse structured fields
        current_section = 'header'
        body_lines = []
        collecting_body = False
        
        for line in lines[1:]:  # Skip header line
            line = line.strip()
            
            # Parse structured fields
            if line.startswith('**TITLE:**'):
                issue_data['title'] = self._extract_field_value(line, '**TITLE:**')
            elif line.startswith('**LABELS:**'):
                labels_str = self._extract_field_value(line, '**LABELS:**')
                issue_data['labels'] = [label.strip() for label in labels_str.split(',') if label.strip()]
            elif line.startswith('**ASSIGNEE:**'):
                issue_data['assignee'] = self._extract_field_value(line, '**ASSIGNEE:**')
            elif line.startswith('**DUE_DATE:**'):
                issue_data['due_date'] = self._extract_field_value(line, '**DUE_DATE:**')
            elif line.startswith('**BODY:**'):
                collecting_body = True
                continue
            elif line.startswith('**PROJECT_FIELDS:**'):
                collecting_body = False
                current_section = 'project_fields'
                continue
            elif line.startswith('```') and collecting_body:
                # Handle code block boundaries in body
                if current_section != 'body_code':
                    current_section = 'body_code'
                else:
                    current_section = 'body'
                body_lines.append(line)
            elif collecting_body or current_section == 'body_code':
                body_lines.append(line)
            elif current_section == 'project_fields' and line.startswith('- '):
                # Parse project field
                field_match = re.match(r'^-\s+([^:]+):\s*(.+)$', line)
                if field_match:
                    field_name = field_match.group(1).strip()
                    field_value = field_match.group(2).strip()
                    issue_data['project_fields'][field_name] = field_value
        
        # Clean up body content
        if body_lines:
            issue_data['body'] = '\n'.join(body_lines).strip()
        
        # Validate required fields
        if not issue_data['title']:
            logger.warning(f"Issue {issue_id} missing title, skipping")
            return None
        
        # Clean up and validate data
        issue_data = self._clean_issue_data(issue_data)
        
        logger.debug(f"Parsed issue: {issue_data['id']} - {issue_data['title']}")
        return issue_data
    
    def _looks_like_issue_section(self, section: str) -> bool:
        """Check if section looks like an issue definition"""
        # Look for key indicators that this is an issue section
        indicators = ['**TITLE:**', '**LABELS:**', '**ASSIGNEE:**', '**BODY:**']
        return any(indicator in section for indicator in indicators)
    
    def _extract_field_value(self, line: str, field_name: str) -> str:
        """Extract value from a field line"""
        return line.replace(field_name, '').strip()
    
    def _clean_issue_data(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate issue data"""
        # Clean assignee field
        if issue_data['assignee']:
            assignee = issue_data['assignee'].strip()
            if assignee == '@me':
                # Will be replaced with actual username during creation
                issue_data['assignee'] = '@me'
            elif not assignee.startswith('@'):
                issue_data['assignee'] = f"@{assignee}"
        
        # Validate due date format
        if issue_data['due_date']:
            try:
                datetime.strptime(issue_data['due_date'], '%Y-%m-%d')
            except ValueError:
                logger.warning(f"Invalid due date format for issue {issue_data['id']}: {issue_data['due_date']}")
                issue_data['due_date'] = ''
        
        # Remove empty labels
        issue_data['labels'] = [label for label in issue_data['labels'] if label]
        
        return issue_data
    
    def filter_issues(self, **filters) -> List[Dict[str, Any]]:
        """Filter issues based on criteria"""
        filtered_issues = self.issues.copy()
        
        for filter_key, filter_value in filters.items():
            if filter_key == 'week':
                # Filter by week (assuming week information is in ID or labels)
                week_pattern = f"week.{filter_value}|w{filter_value}|week-{filter_value}"
                filtered_issues = [
                    issue for issue in filtered_issues
                    if re.search(week_pattern, issue['id'].lower()) or
                       any(re.search(week_pattern, label.lower()) for label in issue['labels'])
                ]
            elif filter_key == 'type':
                # Filter by type (in labels)
                filtered_issues = [
                    issue for issue in filtered_issues
                    if filter_value.lower() in [label.lower() for label in issue['labels']]
                ]
            elif filter_key == 'assignee':
                # Filter by assignee
                filtered_issues = [
                    issue for issue in filtered_issues
                    if issue['assignee'].lower() == filter_value.lower()
                ]
            elif filter_key == 'priority':
                # Filter by priority (in labels or project fields)
                priority_patterns = {
                    'critical': ['critical', '🚨', 'blocker', '🛑'],
                    'high': ['high', '⚠️', '🔥'],
                    'medium': ['medium', '📋'],
                    'low': ['low', '💡']
                }
                
                patterns = priority_patterns.get(filter_value.lower(), [filter_value.lower()])
                filtered_issues = [
                    issue for issue in filtered_issues
                    if any(
                        any(pattern in label.lower() for pattern in patterns)
                        for label in issue['labels']
                    ) or any(
                        any(pattern in str(field_value).lower() for pattern in patterns)
                        for field_value in issue['project_fields'].values()
                    )
                ]
        
        logger.info(f"Filtered to {len(filtered_issues)} issues (from {len(self.issues)} total)")
        return filtered_issues
    
    def to_json(self, filtered_issues: Optional[List[Dict[str, Any]]] = None, 
                indent: int = 2) -> str:
        """Convert issues to JSON format"""
        issues_to_export = filtered_issues if filtered_issues is not None else self.issues
        
        export_data = {
            'metadata': {
                'source_file': self.markdown_file,
                'parsed_at': datetime.now().isoformat(),
                'total_issues': len(issues_to_export)
            },
            'issues': issues_to_export
        }
        
        return json.dumps(export_data, indent=indent, ensure_ascii=False)
    
    def save_json(self, output_file: str, filtered_issues: Optional[List[Dict[str, Any]]] = None):
        """Save issues to JSON file"""
        try:
            json_data = self.to_json(filtered_issues)
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(json_data)
            
            count = len(filtered_issues) if filtered_issues else len(self.issues)
            logger.info(f"Saved {count} issues to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving JSON file: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description='Parse GitHub issues from markdown file')
    parser.add_argument('input_file', help='Input markdown file (consolidated-issues.md)')
    parser.add_argument('-o', '--output', help='Output JSON file (default: issues.json)')
    parser.add_argument('--week', type=int, help='Filter by specific week (1-10)')
    parser.add_argument('--type', help='Filter by issue type (sprint, milestone, etc.)')
    parser.add_argument('--assignee', help='Filter by assignee')
    parser.add_argument('--priority', help='Filter by priority (critical, high, medium, low)')
    parser.add_argument('--preview', action='store_true', help='Preview parsed issues without saving')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Parse issues
        issue_parser = IssueParser(args.input_file)
        issues = issue_parser.parse_markdown()
        
        if not issues:
            logger.warning("No issues found in the markdown file")
            return 1
        
        # Apply filters
        filters = {}
        if args.week:
            filters['week'] = args.week
        if args.type:
            filters['type'] = args.type
        if args.assignee:
            filters['assignee'] = args.assignee
        if args.priority:
            filters['priority'] = args.priority
        
        if filters:
            issues = issue_parser.filter_issues(**filters)
        
        # Preview mode
        if args.preview:
            print(f"\n📋 Found {len(issues)} issues:")
            print("=" * 50)
            for issue in issues[:10]:  # Show first 10
                print(f"ID: {issue['id']}")
                print(f"Title: {issue['title']}")
                print(f"Labels: {', '.join(issue['labels'])}")
                print(f"Assignee: {issue['assignee']}")
                print(f"Due Date: {issue['due_date']}")
                if issue['project_fields']:
                    print(f"Project Fields: {len(issue['project_fields'])} fields")
                print("-" * 30)
            
            if len(issues) > 10:
                print(f"... and {len(issues) - 10} more issues")
            
            return 0
        
        # Save to JSON
        output_file = args.output or 'issues.json'
        issue_parser.save_json(output_file, issues)
        
        print(f"✅ Successfully parsed and saved {len(issues)} issues to {output_file}")
        return 0
        
    except Exception as e:
        logger.error(f"Failed to parse issues: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
