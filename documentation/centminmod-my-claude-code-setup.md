Source: https://github.com/centminmod/my-claude-code-setup

Scraped on: 2025-10-16

---

# centminmod/my-claude-code-setup

Shared starter template configuration and CLAUDE.md memory bank system for Claude Code

## Overview

My Claude Code project's starter settings and Claude Code hooks and slash commands are provided in this repository for users to try out.

## Quick Start

1. Copy the files in this Github repo to your project directory (where you intended codebase will be).
2. Modify the template files and CLAUDE.md to your liking. `.claude/settings.json` needs to install Terminal-Notifier for macOS https://github.com/centminmod/terminal-notifier-setup. If you're not using macOS, you can remove `.claude/settings.json`.
3. After launching Claude Code for the first time within your project directory, run `/init` so that Claude Code analyses your code base and then populates your memory bank system files as per CLAUDE.md instructions.
4. Optional step highly recommended: Install Visual Studio Code and Claude Code VSC Extension.
5. Optional step highly recommended: Sign up for Github.com account and install Git for Visual Studio Code.
6. CLAUDE.md updated to instruct models to use faster tools so for macOS: `brew install ripgrep fd jq`

## Features

### Claude Code Hooks

The Claude Code hook is for `STOP` which uses Terminal-Notifier to show macOS desktop notifications whenever Claude Code stops and finishes it's response.

### Claude Code Subagents

Claude Code subagents are specialized tools designed to handle complex, multi-step tasks autonomously.

#### memory-bank-synchronizer
- Synchronizes memory bank documentation with actual codebase state
- Pattern documentation synchronization
- Architecture decision updates
- Technical specification alignment
- Implementation status tracking
- Code example freshness validation
- Cross-reference validation

#### code-searcher
- Efficient codebase navigation and search
- Function and class location
- Code pattern identification
- Bug source location assistance
- Feature implementation analysis
- Integration point discovery
- Chain of Draft (CoD) mode for ultra-concise reasoning with minimal tokens

#### get-current-datetime
- Simple DateTime utility for accurate Brisbane, Australia (GMT+10) timezone values
- Execute `TZ='Australia/Brisbane' date` commands
- Provide accurate Brisbane timezone timestamps
- Support multiple format options (default, filename, readable, ISO)

#### ux-design-expert
- UX flow optimization and friction reduction
- Premium UI design with sophisticated visual hierarchies
- Scalable design systems architecture using Tailwind CSS
- Data visualization strategy with Highcharts implementations
- Accessibility compliance and performance optimization
- Component library design with atomic methodology

### Claude Code Slash Commands

#### `/anthropic` Commands
- **`/apply-thinking-to`** - Expert prompt engineering specialist
- **`/convert-to-todowrite-tasklist-prompt`** - Converts complex prompts into efficient TodoWrite tasklist-based methods
- **`/update-memory-bank`** - Simple command to update CLAUDE.md and memory bank files

#### `/ccusage` Commands
- **`/ccusage-daily`** - Generates comprehensive Claude Code usage cost analysis and statistics

#### `/cleanup` Commands
- **`/cleanup-context`** - Memory bank optimization specialist for reducing token usage

#### `/documentation` Commands
- **`/create-readme-section`** - Generate specific sections for README files

#### `/security` Commands
- **`/security-audit`** - Perform comprehensive security audit
- **`/check-best-practices`** - Analyze code against language-specific best practices
- **`/secure-prompts`** - Enterprise-grade security analyzer for detecting prompt injection attacks

#### `/architecture` Commands
- **`/explain-architecture-pattern`** - Identify and explain architectural patterns

#### `/promptengineering` Commands
- **`/convert-to-test-driven-prompt`** - Transform requests into TDD style prompts
- **`/batch-operations-prompt`** - Optimize prompts for multiple file operations

#### `/refactor` Commands
- **`/refactor-code`** - Analysis-only refactoring specialist

## Claude Code Plan Weekly Rate Limits

| Plan | Sonnet 4 (hrs/week) | Opus 4 (hrs/week) |
| --- | --- | --- |
| Pro | 40–80 | – |
| Max ($100 /mo) | 140–280 | 15–35 |
| Max ($200 /mo) | 240–480 | 24–40 |

## Claude Code MCP Servers

### Gemini CLI MCP Server
```bash
claude mcp add gemini-cli /path/to/.venv/bin/python /path/to/mcp_server.py -s user -e GEMINI_API_KEY='GEMINI_API_KEY' -e OPENROUTER_API_KEY='OPENROUTER_API_KEY'
```

### Cloudflare MCP Documentation
```bash
claude mcp add --transport sse cf-docs https://docs.mcp.cloudflare.com/sse -s user
```

### Context 7 MCP Server
```bash
claude mcp add --transport sse context7 https://mcp.context7.com/sse -s user
```

### Notion MCP Server
```bash
claude mcp add-json notionApi '{"type":"stdio","command":"npx","args":["-y","@notionhq/notion-mcp-server"],"env":{"OPENAPI_MCP_HEADERS":"{\"Authorization\": \"Bearer ntn_API_KEY\", \"Notion-Version\": \"2022-06-28\"}"}}' -s user
```

### Chrome Devtools MCP Server
```bash
claude --mcp-config .claude/mcp/chrome-devtools.json
```

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/overview)
- [GitHub Repository](https://github.com/centminmod/my-claude-code-setup)
- Stars: 1.2k
- Forks: 109
- License: MIT
