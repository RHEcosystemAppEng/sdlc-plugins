# Changes Log

## Sections Added to CLAUDE.md

### 1. Project Configuration (top-level heading)
- **Action**: Added
- **Reason**: No existing `# Project Configuration` section found in CLAUDE.md

### 2. Repository Registry
- **Action**: Added (empty table with headers only)
- **Reason**: No Serena MCP servers discovered; user chose to continue without code intelligence
- **Content**: Table with columns Repository, Role, Serena Instance, Path — no data rows

### 3. Jira Configuration
- **Action**: Added
- **Reason**: No existing Jira Configuration found
- **Fields set**:
  - Project key: MYPROJ
  - Cloud ID: abc123
  - Feature issue type ID: 10001
- **Fields omitted** (not provided by user):
  - Git Pull Request custom field
  - GitHub Issue custom field

### 4. Code Intelligence
- **Action**: Added
- **Reason**: No existing Code Intelligence section found
- **Content**: Notice that no Serena MCP servers are configured and code intelligence is not available
- **Subsection**: Limitations — "No limitations known — no Serena instances configured"

### 5. Bug Configuration
- **Action**: Added
- **Reason**: No existing Bug Configuration found
- **Fields set**:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

## Sections Not Created

### Jira Field Defaults
- **Reason**: No MCP or REST API available to discover priorities and fixVersions

### Hierarchy Configuration
- **Reason**: No MCP or REST API available to discover issue type hierarchy

### Security Configuration
- **Reason**: User declined to enable security triage

## Files Not Modified (Simulation Mode)

- `docs/constraints.md` — would have been created from constraints template
- `docs/bug-template.md` — would have been created from bug template
- `CONVENTIONS.md` — scaffolding skipped (no Serena instances for analysis)
