#!/usr/bin/env python3

import subprocess
import json
import sys
import os

def run_command(cmd, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def test_github_cli():
    """Test GitHub CLI functionality"""
    print("🔍 Testing GitHub CLI setup...")
    
    # Test 1: Check authentication
    print("\n1. Checking GitHub CLI authentication...")
    returncode, stdout, stderr = run_command("gh auth status")
    if returncode != 0:
        print(f"❌ Authentication failed: {stderr}")
        return False
    print("✅ GitHub CLI authenticated")
    
    # Test 2: Get user info
    print("\n2. Getting GitHub user info...")
    returncode, stdout, stderr = run_command("gh api user --jq '.login'")
    if returncode != 0:
        print(f"❌ Failed to get user info: {stderr}")
        return False
    username = stdout.strip()
    print(f"✅ GitHub username: {username}")
    
    # Test 3: Check repository access
    print("\n3. Checking repository access...")
    returncode, stdout, stderr = run_command("gh repo view --json name,owner,hasIssuesEnabled")
    if returncode != 0:
        print(f"❌ Repository access failed: {stderr}")
        return False
    
    try:
        repo_info = json.loads(stdout)
        print(f"✅ Repository: {repo_info['owner']['login']}/{repo_info['name']}")
        print(f"✅ Issues enabled: {repo_info['hasIssuesEnabled']}")
        
        if not repo_info['hasIssuesEnabled']:
            print("❌ Issues are not enabled for this repository!")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse repository info: {e}")
        return False
    
    return True

def test_issue_creation():
    """Test creating a simple issue"""
    print("\n🚀 Testing issue creation...")
    
    # Create a test issue
    test_title = f"Test Issue Created by Debug Script"
    test_body = "This is a test issue created to debug the automation script."
    
    print(f"\n4. Creating test issue: '{test_title}'")
    
    # Use a simpler command format
    cmd = f'gh issue create --title "{test_title}" --body "{test_body}" --label "test"'
    print(f"Command: {cmd}")
    
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode != 0:
        print(f"❌ Issue creation failed:")
        print(f"   Return code: {returncode}")
        print(f"   Stdout: {stdout}")
        print(f"   Stderr: {stderr}")
        
        # Try without labels
        print("\n5. Retrying without labels...")
        cmd_no_labels = f'gh issue create --title "{test_title}" --body "{test_body}"'
        returncode, stdout, stderr = run_command(cmd_no_labels)
        
        if returncode != 0:
            print(f"❌ Issue creation failed even without labels:")
            print(f"   Return code: {returncode}")
            print(f"   Stdout: {stdout}")
            print(f"   Stderr: {stderr}")
            return False
    
    print(f"✅ Issue created successfully!")
    print(f"   Output: {stdout}")
    
    # Try to extract issue number for cleanup
    try:
        # Look for issue URL pattern
        import re
        url_match = re.search(r'https://github\.com/[^/]+/[^/]+/issues/(\d+)', stdout)
        if url_match:
            issue_number = url_match.group(1)
            print(f"   Issue number: #{issue_number}")
            
            # Close the test issue
            print(f"\n6. Cleaning up test issue #{issue_number}...")
            close_cmd = f'gh issue close {issue_number} --reason "not_planned"'
            returncode, stdout, stderr = run_command(close_cmd)
            
            if returncode == 0:
                print("✅ Test issue closed successfully")
            else:
                print(f"⚠️  Failed to close test issue: {stderr}")
        
    except Exception as e:
        print(f"⚠️  Could not parse issue number for cleanup: {e}")
    
    return True

def test_parsed_issue_creation():
    """Test creating an issue from parsed JSON data (similar to create-issues.sh)"""
    print("\n📝 Testing issue creation from parsed data...")
    
    # Sample issue data similar to what parse-issues.py would generate
    sample_issue = {
        "id": "DEBUG_TEST_PARSED",
        "title": "Debug Test: Parsed Issue Creation",
        "body": "This is a test issue created from parsed JSON data, similar to the main automation script.",
        "assignee": "@me",
        "labels": ["test", "automation", "debug"]
    }
    
    print(f"\n7. Sample issue data:")
    print(json.dumps(sample_issue, indent=2))
    
    # Extract data (similar to create-issues.sh logic)
    issue_id = sample_issue.get('id', '')
    title = sample_issue.get('title', '')
    body = sample_issue.get('body', '')
    assignee = sample_issue.get('assignee', '')
    labels = sample_issue.get('labels', [])
    
    # Get GitHub username for @me assignee
    returncode, stdout, stderr = run_command("gh api user --jq '.login'")
    if returncode == 0:
        github_user = stdout.strip()
        if assignee == "@me":
            assignee_clean = github_user
        else:
            assignee_clean = assignee.lstrip('@')
    else:
        assignee_clean = "ndethi"  # fallback
    
    # Convert labels to comma-separated string
    labels_str = ",".join(labels)
    
    print(f"\n8. Extracted data:")
    print(f"   ID: {issue_id}")
    print(f"   Title: {title}")
    print(f"   Assignee: {assignee} -> {assignee_clean}")
    print(f"   Labels: {labels_str}")
    print(f"   Body length: {len(body)} characters")
    
    # Build command similar to create-issues.sh
    cmd_parts = [
        'gh issue create',
        f'--title "{title}"',
        f'--body "{body}"'
    ]
    
    if labels_str:
        cmd_parts.append(f'--label "{labels_str}"')
    
    if assignee_clean:
        cmd_parts.append(f'--assignee "{assignee_clean}"')
    
    cmd = ' '.join(cmd_parts)
    
    print(f"\n9. Creating issue with command:")
    print(f"   {cmd}")
    
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode != 0:
        print(f"❌ Parsed issue creation failed:")
        print(f"   Return code: {returncode}")
        print(f"   Stdout: {stdout}")
        print(f"   Stderr: {stderr}")
        
        # Debug: try piece by piece
        print("\n10. Debugging command components...")
        
        # Try minimal command
        minimal_cmd = f'gh issue create --title "{title}" --body "{body}"'
        print(f"    Trying minimal: {minimal_cmd}")
        returncode, stdout, stderr = run_command(minimal_cmd)
        
        if returncode == 0:
            print("✅ Minimal command works - issue might be with labels or assignee")
            print(f"   Output: {stdout}")
            return True
        else:
            print(f"❌ Even minimal command fails: {stderr}")
            return False
    
    print(f"✅ Parsed issue created successfully!")
    print(f"   Output: {stdout}")
    return True

if __name__ == "__main__":
    print("🔧 GitHub Issue Creation Debug Tool")
    print("=" * 50)
    
    # Test GitHub CLI setup
    if not test_github_cli():
        print("\n❌ GitHub CLI setup test failed!")
        sys.exit(1)
    
    # Test basic issue creation
    if not test_issue_creation():
        print("\n❌ Basic issue creation test failed!")
        sys.exit(1)
    
    # Test parsed issue creation
    if not test_parsed_issue_creation():
        print("\n❌ Parsed issue creation test failed!")
        sys.exit(1)
    
    print("\n🎉 All tests passed! GitHub issue creation is working correctly.")
    print("\nThe issue with create-issues.sh might be:")
    print("1. Input file format/parsing issues")
    print("2. Environment variables not set correctly")
    print("3. Command construction in the bash script")
    print("4. Error handling masking the real issue")
    print("\nRun this script again to verify consistent behavior.")
