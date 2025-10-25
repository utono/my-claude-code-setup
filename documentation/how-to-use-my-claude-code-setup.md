# How to Use My Claude Code Setup
<!-- File: /home/mlj/utono/mccs-fork-manager/documentation/how-to-use-my-claude-code-setup.md -->

## Overview

This guide documents a fork management system for maintaining a customized version of `centminmod/my-claude-code-setup`. The upstream repository provides an enhanced Claude Code setup with 20+ slash commands, 4 specialized subagents, Chrome DevTools MCP configuration, and a comprehensive memory bank system.

**The Challenge:** The upstream repository is actively maintained and receives frequent updates. You want to benefit from these upstream improvements while maintaining your own substantial customizations. Simply forking and modifying leads to merge conflicts and makes it difficult to selectively incorporate upstream changes.

**The Solution:** A fork management project that acts as an intermediary layer between the upstream repository and your working directories. This approach separates upstream tracking from customization, provides a controlled merge process, and enables clean deployment to multiple projects via rsync.

## Fork Management Setup

This section describes the complete workflow for maintaining your fork with customizations while staying synchronized with `centminmod/my-claude-code-setup`.

### Understanding the Fork Management Workflow

The fork management system uses a three-layer architecture that separates concerns and provides clean integration points:

```
upstream (centminmod/my-claude-code-setup)
    ↓ (fetch/merge updates)
your-fork/master branch (tracks upstream)
    ↓ (merge into)
your-fork/customizations branch (your modifications)
    ↓ (rsync --exclude=.git)
~/target-directory (actual working copy)
```

**Benefits:**
- **Track upstream** - Keep `master` branch synced with centminmod's repo
- **Isolate customizations** - All your changes in `customizations` branch
- **Merge strategy** - Regularly merge `master` → `customizations` to get updates
- **Deploy separately** - Use rsync to copy merged result to working directory
- **Version control** - Full Git history for your customizations
- **Conflict resolution** - Handle merge conflicts in fork, not working directory

### Initial Fork Setup

#### 1. Set Up .gitignore in Fork Manager

**IMPORTANT:** The fork management project itself should NOT commit the fork directory. Create a `.gitignore` file:

```bash
cd $HOME/utono/mccs-fork-manager

# Create .gitignore to exclude the fork
cat > .gitignore <<'EOF'
# Fork repository (managed independently)
my-claude-code-setup/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
*.tmp
*.temp
*.log
EOF

# Commit the .gitignore (if mccs-fork-manager is a git repo)
git add .gitignore
git commit -m "chore: ignore fork directory in fork manager"
```

**Why this is critical:**
- The fork (`my-claude-code-setup/`) has its own `.git` directory and history
- The fork manager project should only track its documentation and scripts
- Prevents nested Git repository issues and conflicts
- Keeps the fork's Git history separate from the manager's Git history
- Without this, you risk committing 100s of files from the fork into the manager repo

#### 2. Clone Your Fork

```bash
# Clone your fork (replace <your-username> with your GitHub username)
git clone https://github.com/<your-username>/my-claude-code-setup.git $HOME/utono/mccs-fork-manager/my-claude-code-setup
cd $HOME/utono/mccs-fork-manager/my-claude-code-setup
```

#### 3. Add Upstream Remote

```bash
# Add the original centminmod repo as upstream
git remote add upstream https://github.com/centminmod/my-claude-code-setup.git

# Verify remotes
git remote -v
# Should show:
# origin    https://github.com/<your-username>/my-claude-code-setup.git (fetch)
# origin    https://github.com/<your-username>/my-claude-code-setup.git (push)
# upstream  https://github.com/centminmod/my-claude-code-setup.git (fetch)
# upstream  https://github.com/centminmod/my-claude-code-setup.git (push)
```

#### 4. Create Customizations Branch

```bash
# Create and checkout the customizations branch
git checkout -b customizations

# Push to your fork
git push -u origin customizations
```

### Ongoing Sync Workflow

#### Syncing Upstream Updates

```bash
# 1. Switch to master branch
git checkout master

# 2. Fetch upstream changes
git fetch upstream

# 3. Merge upstream into your master
git merge upstream/master

# 4. Push updates to your fork (optional)
git push origin master

# 5. Switch to customizations branch
git checkout customizations

# 6. Merge master into customizations
git merge master

# If conflicts occur, resolve them, then:
# git add .
# git commit -m "Merge upstream updates into customizations"

# 7. Push customizations to your fork (optional)
git push origin customizations
```

#### Making Your Own Customizations

```bash
# Always work in the customizations branch
git checkout customizations

# Make your changes
# edit files...

# Commit your changes
git add .
git commit -m "feat: add custom slash command for XYZ"
git push origin customizations
```

#### Deploying to Working Directory

After merging upstream updates and resolving any conflicts:

```bash
# From the customizations branch
cd $HOME/utono/mccs-fork-manager/my-claude-code-setup
git checkout customizations

# Deploy to your actual working directory (adjust path as needed)
rsync -av --exclude='.git' --exclude='README.md' --exclude='GEMINI.md' --exclude='LICENSE' --exclude='.claude/settings.json' ~/utono/mccs-fork-manager/my-claude-code-setup/ <your-project-directory>/

# Or deploy to a new project
rsync -av --exclude='.git' --exclude='README.md' --exclude='GEMINI.md' --exclude='LICENSE' --exclude='.claude/settings.json' ~/utono/mccs-fork-manager/my-claude-code-setup/ <new-project-dir>/
```

### Automation Script (Optional)

Create `$HOME/utono/mccs-fork-manager/sync-fork.sh`:

```bash
#!/bin/bash
# File: $HOME/utono/mccs-fork-manager/sync-fork.sh

set -e  # Exit on error

FORK_DIR="$HOME/utono/mccs-fork-manager/my-claude-code-setup"
DEPLOY_TARGET="$HOME/.claude-code-setup"

echo "🔄 Syncing fork with upstream..."
cd "$FORK_DIR"

# Update master branch
git checkout master
git fetch upstream
git merge upstream/master
echo "✅ Master branch updated"

# Merge into customizations
git checkout customizations
if git merge master; then
    echo "✅ Merged master into customizations (no conflicts)"
else
    echo "❌ Merge conflicts detected. Resolve manually, then run:"
    echo "   git add . && git commit -m 'Merge upstream updates'"
    exit 1
fi

# Optional: Deploy to working directory
read -p "Deploy to $DEPLOY_TARGET? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rsync -av --exclude='.git' --exclude='README.md' --exclude='GEMINI.md' --exclude='LICENSE' --exclude='.claude/settings.json' ./ "$DEPLOY_TARGET"/
    echo "✅ Deployed to $DEPLOY_TARGET"
fi

echo "✅ Fork sync complete!"
```

Make it executable:
```bash
chmod +x $HOME/utono/mccs-fork-manager/sync-fork.sh
```

Usage:
```bash
# Sync and optionally deploy
$HOME/utono/mccs-fork-manager/sync-fork.sh
```

### Checking Fork Status

```bash
cd $HOME/utono/mccs-fork-manager/my-claude-code-setup

# Check current branch and status
git status

# See commits in customizations not in master
git log master..customizations

# See commits in upstream not yet merged
git fetch upstream
git log master..upstream/master

# Compare your customizations with upstream
git diff upstream/master..customizations
```

### Verifying .gitignore Works

After setting up `.gitignore`, verify the fork directory is properly excluded:

```bash
cd $HOME/utono/mccs-fork-manager

# This should NOT show my-claude-code-setup/ in the output
git status

# The fork directory should appear in "Untracked files" initially, then disappear after .gitignore is committed
# After .gitignore is committed, git status should be clean (or only show documentation/scripts)
```

### Common Scenarios

**Scenario 1: Upstream updated, no conflicts**
```bash
git checkout master && git fetch upstream && git merge upstream/master
git checkout customizations && git merge master
# Deploy with rsync
```

**Scenario 2: Upstream updated, conflicts in your customizations**
```bash
git checkout master && git fetch upstream && git merge upstream/master
git checkout customizations && git merge master
# Resolve conflicts in editor
git add .
git commit -m "Merge upstream updates, resolved conflicts"
# Deploy with rsync
```

**Scenario 3: You made custom changes**
```bash
git checkout customizations
# Make changes
git add .
git commit -m "feat: custom modification"
git push origin customizations
# Deploy with rsync
```

**Scenario 4: Start fresh from upstream**
```bash
git checkout customizations
git reset --hard origin/master  # ⚠️ DESTROYS your customizations!
# Only do this if you want to abandon your changes
```

## Quick Setup for New Projects

### 1. Copy Template Files

Use this rsync command to copy the Claude Code setup to your new project directory:

```bash
rsync -av --exclude='.git' --exclude='README.md' --exclude='GEMINI.md' --exclude='LICENSE' --exclude='.claude/settings.json' $HOME/utono/mccs-fork-manager/my-claude-code-setup/ <new-project-dir>/
```

**What gets copied:**
- ✅ `.claude/` directory (agents, commands, settings.local.json, MCP config)
- ✅ `CLAUDE.md` (AI guidance and memory bank system)
- ✅ `.clinerules` (Cline-specific rules)
- ✅ `.dockerignore` (Docker configuration)
- ✅ `reports/` directory structure

**What gets excluded:**
- ❌ `.git/` (template's git history)
- ❌ `README.md` (template documentation)
- ❌ `GEMINI.md` (template-specific file)
- ❌ `LICENSE` (template's license)
- ❌ `.claude/settings.json` (template-specific settings)

### 2. Initialize Claude Code

```bash
cd <new-project-dir>
# Launch Claude Code and run:
/init
```

The `/init` command will:
- Activate all 20+ slash commands
- Load 4 specialized subagents
- Apply enhanced CLAUDE.md guidance
- Set up the memory bank system

### 3. Customize for Your Project

#### Update CLAUDE.md
Edit the "Project Overview" section to describe your specific project:

```markdown
## Project Overview

*Replace this section with your specific project details, architecture, and any domain-specific guidance for AI assistants.*

**Template Notes:**
- Describe your project's purpose, architecture, and key technologies
- Include any project-specific conventions or patterns
- Note important directories, configuration files, or deployment processes
- Optional MCP servers (Context7, Gemini CLI, etc.) can be installed separately - see README.md
```

#### Configure Settings (Optional)
Create `.claude/settings.local.json` for project-specific settings:

```json
{
  "env": {
    "MAX_MCP_OUTPUT_TOKENS": "60000",
    "BASH_DEFAULT_TIMEOUT_MS": "300000",
    "BASH_MAX_TIMEOUT_MS": "600000",
    "MAX_THINKING_TOKENS": "8192"
  },
  "includeCoAuthoredBy": false,
  "permissions": {
    "allow": [
      "Bash(.venv/bin/pip:*)",
      "Bash(.venv/bin/python:*)",
      "Bash(awk:*)",
      "Bash(cat:*)",
      "Bash(ccusage daily)",
      "Bash(ccusage daily:*)",
      "Bash(chmod:*)",
      "Bash(claude config get)",
      "Bash(claude mcp:*)",
      "Bash(cp:*)",
      "Bash(curl:*)",
      "Bash(echo:*)",
      "Bash(env)",
      "Bash(find:*)",
      "Bash(gemini:*)",
      "Bash(grep:*)",
      "Bash(gtimeout:*)",
      "Bash(ls:*)",
      "Bash(mcp:*)",
      "Bash(mkdir:*)",
      "Bash(mv:*)",
      "Bash(pip install:*)",
      "Bash(python:*)",
      "Bash(rg:*)",
      "Bash(sed:*)",
      "Bash(source:*)",
      "Bash(timeout:*)",
      "Bash(tree:*)",
      "Bash(true)",
      "Bash(uv pip install:*)",
      "Bash(uv run:*)",
      "Bash(uv venv:*)",
      "mcp__cf-docs__search_cloudflare_documentation",
      "mcp__context7__get-library-docs",
      "mcp__context7__resolve-library-id",
      "mcp__gemini-cli__gemini_ai_collaboration",
      "mcp__gemini-cli__gemini_cli",
      "mcp__gemini-cli__gemini_help",
      "mcp__gemini-cli__gemini_metrics",
      "mcp__gemini-cli__gemini_models",
      "mcp__gemini-cli__gemini_openrouter_models",
      "mcp__gemini-cli__gemini_openrouter_opinion",
      "mcp__gemini-cli__gemini_openrouter_usage_stats",
      "mcp__gemini-cli__gemini_prompt",
      "mcp__gemini-cli__gemini_review_code",
      "mcp__gemini-cli__gemini_summarize",
      "mcp__gemini-cli__gemini_summarize_files",
      "mcp__gemini-cli__gemini_verify_solution",
      "mcp__gemini-cli__gemini_version",
      "mcp__ide__getDiagnostics",
      "WebFetch(domain:docs.anthropic.com)",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:openrouter.ai)",
      "WebFetch(domain:www.comet.com)",
      "Bash(mkdir:*)",
      "mcp__chrome-devtools__list_pages",
      "mcp__chrome-devtools__navigate_page",
      "mcp__chrome-devtools__take_snapshot",
      "mcp__chrome-devtools__take_screenshot",
      "mcp__chrome-devtools__list_console_messages",
      "mcp__chrome-devtools__list_network_requests",
      "mcp__chrome-devtools__click",
      "mcp__chrome-devtools__fill_form",
      "mcp__chrome-devtools__hover",
      "mcp__chrome-devtools__emulate_cpu",
      "mcp__chrome-devtools__emulate_network",
      "mcp__chrome-devtools__evaluate_script",
      "mcp__chrome-devtools__resize_page",
      "mcp__chrome-devtools__fill",
      "mcp__chrome-devtools__navigate_page_history",
      "mcp__chrome-devtools__new_page"
    ],
    "deny": []
  }
}
```

**Configuration Notes:**
- **Environment variables**: Extended timeouts and token limits for complex operations
- **Permissions**: Pre-approved tools including Chrome DevTools MCP, Gemini CLI, Context7, Cloudflare docs
- **Note**: MCP permissions listed here require those servers to be installed separately (see README.md)

## File Structure Reference

### Reports Directory (`reports/`)

The `reports/` directory contains output from security and analysis commands:

- **`reports/secure-prompts/`** - Security analysis reports from `/secure-prompts` command
  - Example: `security-analysis_20250719_072359.md` - Timestamped security analysis reports with comprehensive threat detection, risk assessment, decoded payloads, and mitigation recommendations

Reports are automatically generated with timestamps in `YYYYMMDD_HHMMSS` format and include both human-readable markdown summaries and complete JSON analysis data.

### Claude Configuration (`.claude/`)

#### Agents (`.claude/agents/`)

Specialized subagents that handle complex autonomous tasks:

- **`code-searcher.md`** - Elite code search specialist with Chain of Draft (CoD) methodology support
  - Standard mode: Comprehensive codebase analysis with exact line numbers
  - CoD mode: 80-92% token reduction for large-scale searches
  - Features: Function/class location, bug investigation, architecture analysis, security analysis, dependency tracing
  - Templates for 6 common search patterns

- **`memory-bank-synchronizer.md`** - Synchronizes memory bank documentation with actual codebase state
  - Ensures architectural patterns match implementation
  - Updates technical decisions to reflect current code
  - Maintains consistency between CLAUDE-*.md files and source code

- **`ux-design-expert.md`** - Comprehensive UX/UI design guidance
  - User experience optimization
  - Premium interface design
  - Scalable design systems
  - Data visualization with Highcharts
  - Tailwind CSS implementation

- **`get-current-datetime.md`** - Brisbane timezone utility agent
  - Executes `TZ='Australia/Brisbane' date` command
  - Returns raw output without formatting

#### Commands (`.claude/commands/`)

Slash commands organized by category:

**Anthropic Commands** (`.claude/commands/anthropic/`)
- **`apply-thinking-to.md`** - Enhances prompts with thinking patterns for better reasoning
- **`convert-to-todowrite-tasklist-prompt.md`** - Transforms requests into structured task lists (60-70% speed improvements)
- **`update-memory-bank.md`** - Updates CLAUDE.md and memory bank files

**Architecture Commands** (`.claude/commands/architecture/`)
- **`explain-architecture-pattern.md`** - Identifies and explains architectural patterns in codebase

**Cost Analysis** (`.claude/commands/ccusage/`)
- **`ccusage-daily.md`** - Analyzes Claude Code usage with markdown reports and cost breakdowns

**Cleanup Commands** (`.claude/commands/cleanup/`)
- **`cleanup-context.md`** - Reduces token usage by 15-25% through context optimization

**Documentation Commands** (`.claude/commands/documentation/`)
- **`create-readme-section.md`** - Generates professional README sections

**Prompt Engineering** (`.claude/commands/promptengineering/`)
- **`batch-operations-prompt.md`** - Optimizes prompts for parallel processing
- **`convert-to-test-driven-prompt.md`** - Transforms prompts into TDD-style development workflow

**Refactoring Commands** (`.claude/commands/refactor/`)
- **`refactor-code.md`** - Analysis-only refactoring plans (does not modify code)

**Security Commands** (`.claude/commands/security/`)
- **`security-audit.md`** - OWASP-based comprehensive security analysis
- **`check-best-practices.md`** - Language-specific code quality checks
- **`secure-prompts.md`** - Advanced prompt injection detection and analysis
  - Multi-layer security framework with role immunity
  - Detects CSS hiding, invisible characters, encoding attacks, role override attempts
  - Generates timestamped reports with risk assessment and mitigation strategies

**Security Test Examples** (`.claude/commands/security/test-examples/`)
- **`test-advanced-injection.md`** - Advanced prompt injection test cases
- **`test-authority-claims.md`** - Authority impersonation detection tests
- **`test-basic-role-override.md`** - Basic role override attempt tests
- **`test-css-hiding.md`** - CSS-based hiding technique tests
- **`test-encoding-attacks.md`** - Encoding obfuscation detection tests (Base64, URL, HTML entities, Unicode)
- **`test-invisible-chars.md`** - Invisible character exploitation tests

#### MCP Configuration (`.claude/mcp/`)

**Pre-configured MCP Servers:**
- **`chrome-devtools.json`** - Chrome DevTools MCP server for browser automation
  - Includes 26 tools for page navigation, screenshots, performance analysis, and debugging
  - Can be dynamically loaded with: `claude --mcp-config .claude/mcp/chrome-devtools.json`
  - Takes ~17K tokens, so only load when needed for browser automation tasks
  - Permissions pre-configured in `settings.local.json` for seamless integration

**Optional MCP Servers** (not included, install separately):
- Context7 - Library documentation (40,000+ libraries)
- Gemini CLI - Multi-model AI collaboration
- Cloudflare Docs - Cloudflare documentation search
- Notion - Notion workspace integration

See upstream README.md for installation commands for optional servers.

#### Settings (`.claude/`)
- **`settings.json`** - Global Claude Code settings
  - Model configuration (sonnet)
  - Hooks configuration (e.g., terminal notifications on session stop)

## What You Get

### 🤖 Specialized Subagents
- **`code-searcher`** - Efficient codebase analysis with Chain of Draft mode (80% token reduction)
- **`memory-bank-synchronizer`** - Keeps documentation synced with code reality
- **`ux-design-expert`** - Comprehensive UX/UI guidance with Tailwind CSS
- **`get-current-datetime`** - Brisbane timezone utility

### ⚡ 20+ Slash Commands

**Security & Best Practices:**
- `/security-audit` - OWASP-based security analysis
- `/check-best-practices` - Language-specific quality checks
- `/secure-prompts` - Prompt injection detection

**Development Workflow:**
- `/refactor-code` - Analysis-only refactoring plans
- `/explain-architecture-pattern` - Architectural pattern identification
- `/cleanup-context` - 15-25% token reduction

**Documentation & Analysis:**
- `/create-readme-section` - Professional README generation
- `/ccusage-daily` - Cost analysis with markdown reports
- `/update-memory-bank` - Synchronize CLAUDE.md and memory files

**Prompt Engineering:**
- `/apply-thinking-to` - Enhanced prompts with thinking patterns
- `/convert-to-todowrite-tasklist-prompt` - 60-70% speed improvements
- `/convert-to-test-driven-prompt` - TDD-style prompt transformation
- `/batch-operations-prompt` - Parallel processing optimization

### 📋 Enhanced AI Guidance
- **Memory bank system** - Structured context management
- **Fast search commands** - Optimized `fd`/`rg` workflows
- **Security-first practices** - Built-in security considerations
- **Chrome DevTools MCP** - Pre-configured for browser automation

## Memory Bank System

The setup includes a structured memory bank system with these core files:

- **CLAUDE-activeContext.md** - Current session state and progress
- **CLAUDE-patterns.md** - Established code patterns and conventions
- **CLAUDE-decisions.md** - Architecture decisions and rationale
- **CLAUDE-troubleshooting.md** - Common issues and solutions
- **CLAUDE-config-variables.md** - Configuration variables reference

Use `/update-memory-bank` to keep these files synchronized with your codebase.

## Example Workflow

```bash
# 1. Set up new project
rsync -av --exclude='.git' --exclude='README.md' --exclude='GEMINI.md' --exclude='LICENSE' --exclude='.claude/settings.json' $HOME/utono/mccs-fork-manager/my-claude-code-setup/ ~/my-new-project/

# 2. Initialize
cd ~/my-new-project
# Launch Claude Code
/init

# 3. Start development with enhanced capabilities
/security-audit                    # Security analysis
/check-best-practices             # Code quality review
/create-readme-section "Installation guide for my React app"
/update-memory-bank               # Keep documentation current

# 4. Optional: Install additional MCP servers
# See README.md for Context7, Gemini CLI, Cloudflare, Notion installations
# Example: claude mcp add --transport sse context7 https://mcp.context7.com/sse -s user
```

## Prerequisites

- Claude Code installed and configured
- Paid Claude AI account (Pro/Max for rate limits)
- macOS: `brew install ripgrep fd jq` for optimized search tools
- Optional: Additional MCP servers (Context7, Gemini CLI, etc.) - see README.md for installation

## Benefits

✅ **Production-ready environment** - Enterprise-grade tooling from day one
✅ **Security-focused** - Built-in security auditing and best practices
✅ **Token-optimized** - Multiple tools for reducing context usage
✅ **Browser automation** - Chrome DevTools MCP pre-configured
✅ **Comprehensive workflows** - 20+ commands cover most development scenarios
✅ **Autonomous capabilities** - Specialized agents handle complex tasks

This setup transforms any project into a fully configured Claude Code environment with professional development workflows, security practices, and up-to-date AI assistance.
