#!/usr/bin/env node

/**
 * GitHub Project Fields Integration
 * Sets custom project fields on GitHub issues using GraphQL API
 */

const { graphql } = require('@octokit/graphql');
const fs = require('fs').promises;
const path = require('path');

// Configuration
const CONFIG = {
    token: process.env.GITHUB_TOKEN,
    owner: '',
    repo: '',
    projectNumber: null,
    dryRun: false,
    verbose: false
};

// Field mappings for different field types
const FIELD_MAPPINGS = {
    'Sprint_Week': { type: 'text' },
    'Criticality': { type: 'single_select' },
    'OPIT_Deadline': { type: 'text' },
    'Thesis_Section': { type: 'single_select' },
    'Effort_Hours': { type: 'number' },
    'Review_Status': { type: 'single_select' }
};

// Logging functions
function log(message, level = 'INFO') {
    const timestamp = new Date().toISOString();
    console.log(`${timestamp} - ${level} - ${message}`);
}

function debug(message) {
    if (CONFIG.verbose) {
        log(message, 'DEBUG');
    }
}

function error(message) {
    log(message, 'ERROR');
}

// GraphQL client setup
function createGraphQLClient() {
    if (!CONFIG.token) {
        throw new Error('GitHub token not found. Set GITHUB_TOKEN environment variable.');
    }
    
    return graphql.defaults({
        headers: {
            authorization: `token ${CONFIG.token}`,
        },
    });
}

// Get repository and project information
async function getRepositoryInfo(client) {
    const query = `
        query($owner: String!, $repo: String!) {
            repository(owner: $owner, name: $repo) {
                id
                owner {
                    projectsV2(first: 10) {
                        nodes {
                            id
                            number
                            title
                        }
                    }
                }
            }
        }
    `;
    
    try {
        const response = await client(query, {
            owner: CONFIG.owner,
            repo: CONFIG.repo
        });
        
        return response.repository;
    } catch (err) {
        throw new Error(`Failed to get repository info: ${err.message}`);
    }
}

// Get project details and fields
async function getProjectDetails(client, projectId) {
    const query = `
        query($projectId: ID!) {
            node(id: $projectId) {
                ... on ProjectV2 {
                    id
                    title
                    fields(first: 20) {
                        nodes {
                            ... on ProjectV2Field {
                                id
                                name
                                dataType
                            }
                            ... on ProjectV2SingleSelectField {
                                id
                                name
                                dataType
                                options {
                                    id
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
    `;
    
    try {
        const response = await client(query, { projectId });
        return response.node;
    } catch (err) {
        throw new Error(`Failed to get project details: ${err.message}`);
    }
}

// Get issue by number
async function getIssue(client, issueNumber) {
    const query = `
        query($owner: String!, $repo: String!, $issueNumber: Int!) {
            repository(owner: $owner, name: $repo) {
                issue(number: $issueNumber) {
                    id
                    number
                    title
                    projectItems(first: 10) {
                        nodes {
                            id
                            project {
                                id
                            }
                        }
                    }
                }
            }
        }
    `;
    
    try {
        const response = await client(query, {
            owner: CONFIG.owner,
            repo: CONFIG.repo,
            issueNumber: parseInt(issueNumber)
        });
        
        return response.repository.issue;
    } catch (err) {
        throw new Error(`Failed to get issue #${issueNumber}: ${err.message}`);
    }
}

// Add issue to project if not already added
async function addIssueToProject(client, projectId, issueId) {
    const mutation = `
        mutation($projectId: ID!, $contentId: ID!) {
            addProjectV2ItemByContentId(input: {
                projectId: $projectId
                contentId: $contentId
            }) {
                item {
                    id
                }
            }
        }
    `;
    
    try {
        const response = await client(mutation, {
            projectId,
            contentId: issueId
        });
        
        return response.addProjectV2ItemByContentId.item.id;
    } catch (err) {
        // Item might already be in project
        if (err.message.includes('already exists')) {
            debug(`Issue already in project: ${issueId}`);
            return null;
        }
        throw new Error(`Failed to add issue to project: ${err.message}`);
    }
}

// Update project field value
async function updateProjectField(client, projectId, itemId, fieldId, value, fieldType = 'text') {
    let mutation;
    let variables = {
        projectId,
        itemId,
        fieldId
    };
    
    switch (fieldType) {
        case 'text':
            mutation = `
                mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
                    updateProjectV2ItemFieldValue(input: {
                        projectId: $projectId
                        itemId: $itemId
                        fieldId: $fieldId
                        value: {
                            text: $value
                        }
                    }) {
                        projectV2Item {
                            id
                        }
                    }
                }
            `;
            variables.value = value.toString();
            break;
            
        case 'number':
            mutation = `
                mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: Float!) {
                    updateProjectV2ItemFieldValue(input: {
                        projectId: $projectId
                        itemId: $itemId
                        fieldId: $fieldId
                        value: {
                            number: $value
                        }
                    }) {
                        projectV2Item {
                            id
                        }
                    }
                }
            `;
            variables.value = parseFloat(value);
            break;
            
        case 'single_select':
            mutation = `
                mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
                    updateProjectV2ItemFieldValue(input: {
                        projectId: $projectId
                        itemId: $itemId
                        fieldId: $fieldId
                        value: {
                            singleSelectOptionId: $optionId
                        }
                    }) {
                        projectV2Item {
                            id
                        }
                    }
                }
            `;
            variables.optionId = value;
            break;
            
        default:
            throw new Error(`Unsupported field type: ${fieldType}`);
    }
    
    try {
        await client(mutation, variables);
        debug(`Updated field ${fieldId} with value: ${value}`);
    } catch (err) {
        throw new Error(`Failed to update field: ${err.message}`);
    }
}

// Find option ID for single select field
function findSelectOption(field, value) {
    if (!field.options) {
        return null;
    }
    
    // Try exact match first
    let option = field.options.find(opt => opt.name === value);
    
    // Try case-insensitive match
    if (!option) {
        option = field.options.find(opt => 
            opt.name.toLowerCase() === value.toLowerCase()
        );
    }
    
    // Try partial match
    if (!option) {
        option = field.options.find(opt => 
            opt.name.toLowerCase().includes(value.toLowerCase()) ||
            value.toLowerCase().includes(opt.name.toLowerCase())
        );
    }
    
    return option ? option.id : null;
}

// Process issues from JSON file
async function processIssuesFromJson(jsonFile) {
    try {
        const data = JSON.parse(await fs.readFile(jsonFile, 'utf8'));
        const issues = data.issues || [];
        
        log(`Processing ${issues.length} issues from ${jsonFile}`);
        
        const client = createGraphQLClient();
        
        // Get repository and project info
        const repoInfo = await getRepositoryInfo(client);
        const projects = repoInfo.owner.projectsV2.nodes;
        
        if (projects.length === 0) {
            throw new Error('No projects found for this repository owner');
        }
        
        // Use specified project or first available
        let project = projects[0];
        if (CONFIG.projectNumber) {
            project = projects.find(p => p.number === CONFIG.projectNumber);
            if (!project) {
                throw new Error(`Project #${CONFIG.projectNumber} not found`);
            }
        }
        
        log(`Using project: ${project.title} (#${project.number})`);
        
        // Get project fields
        const projectDetails = await getProjectDetails(client, project.id);
        const fields = projectDetails.fields.nodes;
        
        debug(`Found ${fields.length} project fields`);
        
        // Process each issue
        let processed = 0;
        let updated = 0;
        
        for (const issueData of issues) {
            try {
                processed++;
                
                // Extract issue number from various formats
                let issueNumber = null;
                if (issueData.github_issue_number) {
                    issueNumber = issueData.github_issue_number;
                } else {
                    // Try to extract from ID or title
                    const match = issueData.id.match(/(\d+)/) || 
                                 issueData.title.match(/#(\d+)/);
                    if (match) {
                        issueNumber = parseInt(match[1]);
                    }
                }
                
                if (!issueNumber) {
                    log(`Skipping issue without number: ${issueData.id}`, 'WARN');
                    continue;
                }
                
                log(`Processing issue #${issueNumber}: ${issueData.title}`);
                
                if (CONFIG.dryRun) {
                    log(`DRY RUN - Would update issue #${issueNumber} with project fields`);
                    continue;
                }
                
                // Get issue details
                const issue = await getIssue(client, issueNumber);
                if (!issue) {
                    log(`Issue #${issueNumber} not found`, 'WARN');
                    continue;
                }
                
                // Add to project if needed
                let projectItem = issue.projectItems.nodes.find(item => 
                    item.project.id === project.id
                );
                
                if (!projectItem) {
                    const itemId = await addIssueToProject(client, project.id, issue.id);
                    if (itemId) {
                        projectItem = { id: itemId };
                    }
                }
                
                if (!projectItem) {
                    log(`Could not add issue #${issueNumber} to project`, 'WARN');
                    continue;
                }
                
                // Update project fields
                const projectFields = issueData.project_fields || {};
                let fieldUpdates = 0;
                
                for (const [fieldName, fieldValue] of Object.entries(projectFields)) {
                    if (!fieldValue) continue;
                    
                    // Find matching project field
                    const projectField = fields.find(f => 
                        f.name === fieldName || 
                        f.name.toLowerCase() === fieldName.toLowerCase()
                    );
                    
                    if (!projectField) {
                        debug(`Project field not found: ${fieldName}`);
                        continue;
                    }
                    
                    try {
                        let processedValue = fieldValue;
                        
                        // Handle single select fields
                        if (projectField.dataType === 'SINGLE_SELECT') {
                            const optionId = findSelectOption(projectField, fieldValue);
                            if (optionId) {
                                processedValue = optionId;
                            } else {
                                log(`Option not found for field ${fieldName}: ${fieldValue}`, 'WARN');
                                continue;
                            }
                        }
                        
                        await updateProjectField(
                            client,
                            project.id,
                            projectItem.id,
                            projectField.id,
                            processedValue,
                            projectField.dataType.toLowerCase()
                        );
                        
                        fieldUpdates++;
                        debug(`Updated ${fieldName}: ${fieldValue}`);
                        
                        // Rate limiting
                        await new Promise(resolve => setTimeout(resolve, 100));
                        
                    } catch (err) {
                        log(`Failed to update field ${fieldName}: ${err.message}`, 'WARN');
                    }
                }
                
                if (fieldUpdates > 0) {
                    updated++;
                    log(`Updated ${fieldUpdates} fields for issue #${issueNumber}`);
                }
                
            } catch (err) {
                log(`Error processing issue: ${err.message}`, 'ERROR');
            }
        }
        
        log(`Completed: ${processed} processed, ${updated} updated`);
        
    } catch (err) {
        error(`Failed to process issues: ${err.message}`);
        throw err;
    }
}

// Main function
async function main() {
    const args = process.argv.slice(2);
    let jsonFile = '';
    
    // Parse arguments
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        const nextArg = args[i + 1];
        
        switch (arg) {
            case '--input':
                jsonFile = nextArg;
                i++;
                break;
            case '--repo':
                const [owner, repo] = nextArg.split('/');
                CONFIG.owner = owner;
                CONFIG.repo = repo;
                i++;
                break;
            case '--project':
                CONFIG.projectNumber = parseInt(nextArg);
                i++;
                break;
            case '--token':
                CONFIG.token = nextArg;
                i++;
                break;
            case '--dry-run':
                CONFIG.dryRun = true;
                break;
            case '--verbose':
            case '-v':
                CONFIG.verbose = true;
                break;
            case '--help':
            case '-h':
                console.log(`
GitHub Project Fields Integration

Usage: node project-fields.js [OPTIONS]

Options:
  --input FILE        JSON file with issue data
  --repo OWNER/REPO   GitHub repository
  --project NUMBER    Project number (default: first project)
  --token TOKEN       GitHub token (or set GITHUB_TOKEN env var)
  --dry-run          Preview changes without applying
  --verbose, -v      Verbose output
  --help, -h         Show this help

Examples:
  node project-fields.js --input issues.json --repo user/repo
  node project-fields.js --input issues.json --repo user/repo --project 1 --dry-run

Environment Variables:
  GITHUB_TOKEN       GitHub personal access token with repo and project permissions
`);
                process.exit(0);
                break;
            default:
                if (!jsonFile && !arg.startsWith('--')) {
                    jsonFile = arg;
                }
                break;
        }
    }
    
    // Validate required arguments
    if (!jsonFile) {
        console.error('Error: Input JSON file is required');
        process.exit(1);
    }
    
    if (!CONFIG.owner || !CONFIG.repo) {
        console.error('Error: Repository (--repo OWNER/REPO) is required');
        process.exit(1);
    }
    
    // Get token from environment if not provided
    if (!CONFIG.token) {
        CONFIG.token = process.env.GITHUB_TOKEN;
    }
    
    if (!CONFIG.token) {
        console.error('Error: GitHub token is required (set GITHUB_TOKEN env var or use --token)');
        process.exit(1);
    }
    
    try {
        await processIssuesFromJson(jsonFile);
        console.log('✅ Project fields integration completed successfully');
    } catch (err) {
        console.error(`❌ Failed: ${err.message}`);
        process.exit(1);
    }
}

// Handle unhandled rejections
process.on('unhandledRejection', (err) => {
    console.error('Unhandled rejection:', err);
    process.exit(1);
});

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = {
    processIssuesFromJson,
    CONFIG
};
