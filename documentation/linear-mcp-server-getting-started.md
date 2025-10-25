# Getting Started with Linear MCP Server

A comprehensive guide to using the Linear MCP server integration with Claude Code.

## Overview

The Linear MCP server enables direct integration between Claude Code and your Linear workspace, allowing you to manage issues, projects, teams, and workflows directly from your coding environment.

## Prerequisites

- Active Linear workspace
- Claude Code with MCP support
- Linear authentication configured (authentication is handled automatically via `/mcp` command)

## Connecting to Linear

Verify your Linear MCP connection:

```bash
/mcp
```

You should see: `Authentication successful. Connected to linear-server.`

## Core Concepts

### Linear Hierarchy
```
Workspace
  ├── Teams
  │     ├── Issues
  │     ├── Projects
  │     ├── Cycles
  │     └── Labels
  └── Users
```

### Available Tools

#### Issues
- `list_issues` - List and filter issues
- `get_issue` - Get detailed issue information
- `create_issue` - Create new issues
- `update_issue` - Update existing issues
- `list_comments` - View issue comments
- `create_comment` - Add comments to issues

#### Projects
- `list_projects` - List projects
- `get_project` - Get project details
- `create_project` - Create new projects
- `update_project` - Update project information

#### Teams & Organization
- `list_teams` - View available teams
- `get_team` - Get team details
- `list_users` - List workspace users
- `get_user` - Get user information

#### Workflow Management
- `list_issue_statuses` - View available issue states
- `get_issue_status` - Get status details
- `list_issue_labels` - View labels
- `create_issue_label` - Create new labels
- `list_cycles` - View team cycles
- `list_project_labels` - View project labels

#### Documentation
- `search_documentation` - Search Linear's official documentation

## Quick Start Workflows

### 1. Explore Your Workspace

```bash
# View your teams
list_teams

# See your assigned issues
list_issues with assignee="me"

# Check current projects
list_projects
```

### 2. Working with Issues

**List issues with filters:**
```bash
# My open issues
list_issues assignee="me" state="In Progress"

# Issues by team
list_issues team="Engineering"

# Recent issues
list_issues updatedAt="-P7D"  # Last 7 days

# Issues by label
list_issues label="bug"

# Search in title/description
list_issues query="authentication"
```

**Get issue details:**
```bash
get_issue id="ABC-123"
```

Returns: Full details including description, attachments, git branch, assignee, state, labels, and more.

**Create an issue:**
```bash
create_issue
  title="Fix login redirect bug"
  team="Engineering"
  description="Users are redirected to wrong page after login"
  assignee="me"
  priority=2  # 1=Urgent, 2=High, 3=Normal, 4=Low
  labels=["bug", "frontend"]
```

**Update an issue:**
```bash
update_issue
  id="ABC-123"
  state="In Progress"
  assignee="me"
```

**Add comments:**
```bash
# List existing comments
list_comments issueId="ABC-123"

# Add a comment
create_comment
  issueId="ABC-123"
  body="Fixed the redirect logic in auth.js"

# Reply to a comment
create_comment
  issueId="ABC-123"
  parentId="comment-id"
  body="Good catch!"
```

### 3. Working with Projects

**List projects:**
```bash
# All active projects
list_projects

# By team
list_projects team="Engineering"

# By state
list_projects state="started"

# My projects
list_projects member="me"

# Search projects
list_projects query="Q1 2025"
```

**Get project details:**
```bash
get_project query="Q1 Roadmap"
```

**Create a project:**
```bash
create_project
  name="Q2 2025 Features"
  team="Engineering"
  summary="Major features for Q2 release"
  description="## Goals\n\n- Feature A\n- Feature B\n- Performance improvements"
  lead="me"
  startDate="2025-04-01"
  targetDate="2025-06-30"
```

**Update a project:**
```bash
update_project
  id="project-id"
  state="started"
  description="Updated goals..."
```

### 4. Team & User Management

**List teams:**
```bash
list_teams
```

**Get team details:**
```bash
get_team query="Engineering"
```

**List users:**
```bash
# All users
list_users

# Search by name/email
list_users query="john"
```

**Get user info:**
```bash
# By name, email, or ID
get_user query="john.doe@example.com"

# Current user
get_user query="me"
```

### 5. Labels & Workflow

**View available labels:**
```bash
# Workspace labels
list_issue_labels

# Team-specific labels
list_issue_labels team="Engineering"

# Filter by name
list_issue_labels name="bug"
```

**Create a label:**
```bash
create_issue_label
  name="technical-debt"
  color="#FF5733"
  description="Code that needs refactoring"
```

**View issue states:**
```bash
list_issue_statuses team="Engineering"
```

**View cycles:**
```bash
# Current cycle
list_cycles teamId="team-id" type="current"

# Next cycle
list_cycles teamId="team-id" type="next"

# All cycles
list_cycles teamId="team-id"
```

## Advanced Filtering

### Date Filters

Use ISO-8601 format or relative durations:

```bash
# Issues created in last day
list_issues createdAt="-P1D"

# Issues updated in last week
list_issues updatedAt="-P7D"

# Projects created after specific date
list_projects createdAt="2025-01-01"
```

### Pagination

Control result sets:

```bash
# Limit results
list_issues limit=10

# With pagination
list_issues after="issue-id" limit=25
list_issues before="issue-id" limit=25
```

### Ordering

```bash
# Order by creation date
list_issues orderBy="createdAt"

# Order by update date (default)
list_issues orderBy="updatedAt"
```

## Common Use Cases

### Daily Standup Workflow

```bash
# Review my tasks
list_issues assignee="me" state="In Progress"

# Update progress
update_issue id="ABC-123" state="In Review"
create_comment issueId="ABC-123" body="Ready for review"

# Check blockers
list_issues assignee="me" priority=1
```

### Bug Triage Workflow

```bash
# List new bugs
list_issues label="bug" state="Backlog"

# Get details
get_issue id="BUG-456"

# Assign and prioritize
update_issue
  id="BUG-456"
  assignee="jane.doe@example.com"
  priority=2
  state="Todo"
```

### Sprint Planning Workflow

```bash
# View current cycle
list_cycles teamId="team-id" type="current"

# Create issues for sprint
create_issue
  title="Implement feature X"
  team="Engineering"
  cycle="Sprint 42"
  assignee="me"
  estimate=5
```

### Project Status Update

```bash
# Get project details
get_project query="Q1 Roadmap"

# Update project status
update_project
  id="project-id"
  state="in_progress"
  summary="50% complete - on track"

# Review project issues
list_issues project="Q1 Roadmap"
```

## Tips & Best Practices

### 1. Use "me" for Current User

Instead of looking up your user ID, use `"me"`:

```bash
list_issues assignee="me"
create_issue assignee="me"
get_user query="me"
```

### 2. Search by Name or ID

Most tools accept names or IDs:

```bash
list_issues team="Engineering"  # By name
list_issues team="team-uuid"    # By ID
```

### 3. Markdown in Descriptions

Use full markdown in issue/project descriptions:

```bash
create_issue
  description="## Bug Details\n\n- Step 1\n- Step 2\n\n```js\ncode here\n```"
```

### 4. Bulk Operations

Use filters to target multiple items:

```bash
# Find all unassigned bugs
list_issues label="bug" assignee=null

# Then assign them
update_issue id="..." assignee="me"
```

### 5. Link Issues to Code

Get git branch names from issues:

```bash
get_issue id="ABC-123"
# Returns: branchName: "abc-123-fix-login-bug"
```

### 6. Use Labels for Organization

Create consistent labeling schemes:

```bash
create_issue_label name="frontend" color="#3B82F6"
create_issue_label name="backend" color="#10B981"
create_issue_label name="bug" color="#EF4444"
create_issue_label name="feature" color="#8B5CF6"
```

### 7. Search Documentation

When unsure about features:

```bash
search_documentation query="issue priorities"
search_documentation query="custom fields"
```

## Troubleshooting

### Connection Issues

```bash
# Re-authenticate
/mcp

# Should return: "Authentication successful. Connected to linear-server."
```

### Finding IDs

Many operations require UUIDs. Use list commands to find them:

```bash
# Get team ID
list_teams

# Get issue ID
list_issues query="specific title"

# Get user ID
list_users query="name or email"
```

### Required Fields

When creating issues/projects, minimum required fields:

**Issues:**
- `title` (required)
- `team` (required)

**Projects:**
- `name` (required)
- `team` (required)

## Examples from Real Workflows

### Example 1: Bug Fix Workflow

```bash
# 1. Find the bug
list_issues query="login timeout" label="bug"

# 2. Get full details
get_issue id="BUG-789"

# 3. Start working on it
update_issue id="BUG-789" state="In Progress" assignee="me"

# 4. Add progress updates
create_comment issueId="BUG-789" body="Identified timeout in session middleware"

# 5. Complete and move to review
update_issue id="BUG-789" state="In Review"
create_comment issueId="BUG-789" body="Fix implemented in PR #123"
```

### Example 2: New Feature Planning

```bash
# 1. Create the feature project
create_project
  name="User Dashboard Redesign"
  team="Design"
  summary="Modernize user dashboard with new components"
  lead="me"
  targetDate="2025-05-01"

# 2. Break down into tasks
create_issue
  title="Design new dashboard layout"
  team="Design"
  project="User Dashboard Redesign"
  assignee="designer@example.com"

create_issue
  title="Implement dashboard components"
  team="Engineering"
  project="User Dashboard Redesign"
  assignee="developer@example.com"

# 3. Track progress
list_issues project="User Dashboard Redesign"
```

### Example 3: Daily Team Sync

```bash
# Show what everyone is working on
list_issues team="Engineering" state="In Progress"

# Show blocked items
list_issues team="Engineering" label="blocked"

# Show items ready for review
list_issues team="Engineering" state="In Review"
```

## Integration with Claude Code Workflows

### When Coding

Ask Claude Code to:
- "Create a Linear issue for this bug"
- "Update Linear issue ABC-123 to in progress"
- "Show me my Linear issues"
- "What's the status of project X?"

### During Code Review

- "Add a comment to Linear issue DEF-456 about this change"
- "Create a follow-up issue for this refactoring"

### Project Management

- "What are the open issues in Q1 Roadmap?"
- "Create a project for the new API development"
- "Show me all high priority bugs assigned to me"

## Additional Resources

- [Linear API Documentation](https://developers.linear.app/)
- [Linear User Guide](https://linear.app/docs)
- Use `search_documentation` for specific feature queries

## Summary

The Linear MCP server provides comprehensive workspace management capabilities directly within Claude Code. Key advantages:

- **No context switching** - Manage issues without leaving your editor
- **Natural language** - Ask Claude Code to perform Linear operations
- **Full CRUD** - Create, read, update issues, projects, and more
- **Advanced filtering** - Find exactly what you need with rich query options
- **Workflow integration** - Connect code changes to Linear issues seamlessly

Start with basic commands like `list_issues` and `list_teams`, then explore advanced workflows as needed.
