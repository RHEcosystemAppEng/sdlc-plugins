# Performance Skills Common Patterns

This document defines reusable patterns used across all performance skills to ensure consistency and reduce duplication.

## Config Schema Reference

The authoritative schema for `performance-config.json` is defined in `scripts/perf-config.py`, constant `DEFAULT_CONFIG` (lines 32–118). All skills MUST use `perf-config.py get/set` subcommands for field access — never read or write the JSON file directly.

---

## Pattern 0: Plugin Root Resolution

**Purpose:** Locate the installed sdlc-workflow plugin root directory at runtime

**When to use:** Once per skill, before any operation that reads plugin files (scripts, templates, shared resources)

**Used by:**
- All skills that use Jira REST API fallback (Pattern 11)
- Skills that read plugin templates or scripts

**Procedure:**

```bash
# Resolve plugin root — works for any registry name and any version
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null \
  | sort -V | tail -1)

if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then
  echo "❌ sdlc-workflow plugin not found in ~/.claude/plugins/cache/"
  echo "   Ensure the plugin is installed and try again."
  exit 1
fi

# $plugin_root is now set, e.g.: /home/user/.claude/plugins/cache/sdlc-plugins-local/sdlc-workflow/0.6.1/
```

**Why this works:**

- Glob `cache/*/sdlc-workflow/*/` matches any registry name (sdlc-plugins-local, sdlc-plugins, marketplace names)
- Matches any version number in the plugin cache
- `sort -V | tail -1` selects the latest version if multiple are present
- Uses `$HOME` for cross-platform compatibility
- Validation ensures the directory exists before proceeding

**Usage in subsequent commands:**

```bash
# Execute plugin scripts
python3 "$plugin_root/scripts/perf-config.py" <subcommand>
python3 "$plugin_root/scripts/jira-client.py" <command>

# Reference a template path (use agent Read tool on this path)
template_path="${plugin_root}skills/performance/baseline-report.template.md"
```

---

## Pattern 1: Config Reading

**Purpose:** Validate that `performance-config.json` exists before skill execution

**When to use:** All skills (typically Step 2)

**Used by:**
- performance-baseline (Step 2)
- performance-analyze-module (Step 2)
- performance-plan-optimization (Step 2)
- performance-implement-optimization (Step 1)
- performance-verify-optimization (Step 6.1)
- performance-setup (Step 2 - detection only)

**Procedure:**

```bash
# Validate performance configuration exists and is valid JSON
python3 "$plugin_root/scripts/perf-config.py" validate
# Exits with error if config missing or invalid
```

**Error handling:**

If config does not exist, inform the user:

> "Performance Analysis Configuration not found. Please run `/sdlc-workflow:performance-setup` first to initialize the configuration, then re-run this skill."

Stop execution.

**Variations:**

- **setup skill**: Checks if config exists to offer update vs skip (Step 2)
- **Other skills**: Config must exist or skill fails

---

## Pattern 2: Metadata Extraction

**Purpose:** Read metadata fields from performance-config.json frontmatter


**Used by:**
- performance-baseline (Step 2.2)
- performance-analyze-module (Step 2.2)
- performance-implement-optimization (Step 9.0.5, Step 9.1)
- performance-verify-optimization (Step 6.2)
- performance-setup (Step 2 - version detection)

**Procedure:**

```bash
# Read metadata from frontmatter
extract metadata.baseline_captured (true | false)
extract metadata.baseline_timestamp (ISO timestamp | null)
extract metadata.baseline_commit_sha (git SHA | null)
extract metadata.backend_available (true | false)
extract metadata.last_updated (ISO timestamp)
```

**Metadata Fields Reference:**

| Field | Type | Description |
|---|---|---|
| `version` | string | Config version identifier |
| `created` | ISO timestamp | When config was first created |
| `last_updated` | ISO timestamp | When config was last modified |
| `workflow_selected` | boolean | Whether workflow has been selected |
| `baseline_captured` | boolean | Whether initial baseline was captured |
| `baseline_timestamp` | ISO timestamp or null | When baseline was captured |
| `baseline_commit_sha` | string or null | Git commit at baseline capture |
| `backend_available` | boolean | Whether backend is configured and accessible |
| `analysis_scope` | string | Determines which repositories are analyzed: "full-stack-monorepo" (same repo), "full-stack" (separate repos), "frontend-only", "backend-only" |

**Error handling:**

- If metadata is malformed, log warning and use defaults

---

## Pattern 3: Mode Consistency Enforcement

**Purpose:** Ensure all baseline captures use the same mode for valid performance comparisons

**When to use:** When capturing performance metrics (baseline, implement re-run, verify re-run)

**Used by:**
- performance-baseline (Step 5.0, Step 5.1)
- performance-implement-optimization (Step 9.1)
- performance-verify-optimization (Step 6.2)

**Procedure:**

```bash
# Read stored mode from metadata (see Pattern 2)
baseline_already_captured = metadata.baseline_captured  # true | false

# If baseline already captured, enforce mode consistency
if baseline_already_captured and stored_mode is not null:
  # Inform user of stored mode
  echo "Previous baseline mode detected: ${stored_mode}"
  echo "For valid comparisons, all captures MUST use the same mode."
  
  # If user tries to select different mode, warn:
  if user_selected_mode != stored_mode:
    echo "⚠️ Mode mismatch detected!"
    echo "Stored mode: ${stored_mode}"
    echo "Selected mode: ${user_selected_mode}"
    echo ""
    echo "Options:"
    echo "1. Use stored mode (${stored_mode}) - Recommended"
    echo "2. Reset baseline (discards previous baseline)"
    echo "3. Cancel"
    
    # Handle user choice
    if choice == 1:
      user_selected_mode = stored_mode
    elif choice == 2:
      # Clear baseline data, allow new mode
      metadata.baseline_captured = false
      metadata.baseline_mode = null
    else:
      exit 0
fi

# Use user_selected_mode for capture
mode = user_selected_mode
```

**Why consistency matters:**

Different modes measure different conditions:
- **cold-start**: Direct URL navigation with cold cache (worst-case, first visit)

Comparing metrics across different modes produces invalid results.

**Error handling:**

- If user chooses mode different from stored mode, warn and offer reset or cancel
- If mode is null (first capture), store user's selection in metadata

---

## Pattern 4: Directory Extraction

**Purpose:** Extract performance artifact directories from configuration

**When to use:** When writing performance reports (baseline, analysis, plans, verification)

**Used by:**
- performance-baseline (Step 8.1)
- performance-analyze-module (Steps 7.1-A/B)
- performance-plan-optimization (Step 6.1)
- performance-implement-optimization (Step 9.1)
- performance-verify-optimization (Step 6.3)

**Procedure:**

```bash
# Read directory paths from JSON config
baseline_dir=$(python3 "$plugin_root/scripts/perf-config.py" get directories.baselines)
analysis_dir=$(python3 "$plugin_root/scripts/perf-config.py" get directories.analysis)
plans_dir=$(python3 "$plugin_root/scripts/perf-config.py" get directories.plans)
verification_dir=$(python3 "$plugin_root/scripts/perf-config.py" get directories.verification)

# Ensure directories exist
mkdir -p "$baseline_dir" "$analysis_dir" "$plans_dir" "$verification_dir"
```

**Standard directory structure:**

```
.claude/performance/
├── baselines/           # Baseline performance reports
├── analysis/            # Module and application analysis reports
├── plans/               # Optimization plan documents
└── verification/        # Verification reports for optimization PRs
```

**Error handling:**

- If directory creation fails (permissions issue), stop execution
- If Target Directories section is missing, use standard paths

---

## Pattern 5: Baseline Report Reading

**Purpose:** Read baseline metrics from baseline-report.md

**When to use:** When comparing current performance against baseline

**Used by:**
- performance-analyze-module (Step 3)
- performance-implement-optimization (Step 9.1, Step 9.2)

**Procedure:**

```bash
# Check if baseline report exists
baseline_report=".claude/performance/baselines/baseline-report.md"

if [ ! -f "$baseline_report" ]; then
  echo "Baseline report not found. Please run /sdlc-workflow:performance-baseline first."
  exit 1
fi

# Read baseline report
report=$(cat "$baseline_report")

# Extract p95 metrics from Performance Metrics section
lcp_p95=$(echo "$report" | grep "LCP (p95)" | awk '{print $4}')
fcp_p95=$(echo "$report" | grep "FCP (p95)" | awk '{print $4}')
tti_p95=$(echo "$report" | grep "DOM Interactive (p95)" | awk '{print $4}')
total_load_p95=$(echo "$report" | grep "Total Load Time (p95)" | awk '{print $4}')

# Extract metadata from YAML frontmatter (between --- delimiters)
frontmatter=$(echo "$report" | sed -n '/^---$/,/^---$/p' | sed '1d;$d')
workflow_name=$(echo "$frontmatter" | grep "workflow:" | awk '{print $2}')
capture_mode=$(echo "$frontmatter" | grep "capture_mode:" | awk '{print $2}')

# Extract baseline timestamp
baseline_timestamp=$(echo "$report" | grep "timestamp:" | awk '{print $2}')
```

**Baseline Report Structure:**

```markdown
---
workflow: {workflow-name}
timestamp: {ISO-timestamp}
commit_sha: {git-commit-sha}
---

# Baseline Performance Report

## Performance Metrics

| Metric | p50 | p75 | p95 | p99 | Unit |
|---|---|---|---|---|---|
| LCP | ... | ... | ... | ... | ms |
| FCP | ... | ... | ... | ... | ms |
| DOM Interactive | ... | ... | ... | ... | ms |
| Total Load Time | ... | ... | ... | ... | ms |
```

**Error handling:**

- If baseline report is missing, stop execution with actionable message
- If metrics are malformed, log warning and use fallback values

---

## Pattern 6: Workflow Validation

**Purpose:** Extract and validate Selected Workflow section from configuration

**When to use:** When skill operates on a specific workflow (most skills)

**Used by:**
- performance-baseline (Step 2.1)
- performance-analyze-module (Step 2.1)
- performance-plan-optimization (Step 2.1)
- performance-implement-optimization (Step 2)

**Procedure:**

```bash
# Verify workflow is selected
workflow_selected=$(python3 "$plugin_root/scripts/perf-config.py" get metadata.workflow_selected)
if [ "$workflow_selected" != "true" ]; then
  echo "No workflow selected for optimization."
  echo "Please run /sdlc-workflow:performance-baseline first to select a workflow."
  exit 1
fi

# Extract workflow details
workflow_name=$(python3 "$plugin_root/scripts/perf-config.py" get workflow.name)
entry_point=$(python3 "$plugin_root/scripts/perf-config.py" get workflow.entry_point)
key_screens=$(python3 "$plugin_root/scripts/perf-config.py" get workflow.key_screens)
complexity=$(python3 "$plugin_root/scripts/perf-config.py" get workflow.complexity)
```

**Selected Workflow Table Format:**

```markdown
## Selected Workflow

The following workflow has been selected for performance optimization:

| Property | Value |
|---|---|
| Workflow Name | {workflow-name} |
| Entry Point | {entry-point-url} |
| Key Screens | {comma-separated-list} |
| Complexity | {complexity-estimate} |
| Selected On | {YYYY-MM-DD} |
```

**Error handling:**

- If Selected Workflow section is missing, stop execution
- If workflow details are incomplete, warn user and attempt to proceed with available data

---

## Pattern 7: Dev Command Approval

**Purpose:** Discover, present, and get user approval for dev mode commands before execution

**When to use:** Before baseline capture when application needs to be running

**Used by:**
- performance-baseline (Step 7.4)
- performance-implement-optimization (Step 9 - before re-running baseline)
- performance-verify-optimization (Step 6 - before re-running baseline)

**Procedure:**

```bash
# Step 1: Check if dev command already configured
dev_command=$(python3 "$plugin_root/scripts/perf-config.py" get dev_environment.command)
command_approved=$(python3 "$plugin_root/scripts/perf-config.py" get dev_environment.command_approved)
if [ "$dev_command" != "null" ]; then
  command_hash=$(python3 "$plugin_root/scripts/perf-config.py" get metadata.dev_command_hash)
  
  # Calculate current hash
  current_hash=$(echo -n "$dev_command" | sha256sum | awk '{print $1}')
  
  # If command unchanged and already approved, skip prompt
  if [ "$command_approved" = "true" ] && [ "$current_hash" = "$command_hash" ]; then
    echo "ℹ️ Dev command already approved: $dev_command"
    skip_to_verification=true
  fi
fi

# Step 2: If not approved or changed, discover dev command
if [ "$skip_to_verification" != "true" ]; then
  discovered_command=""
  doc_source=""
  
  # Check package.json scripts
  if [ -f "package.json" ]; then
    dev_script=$(jq -r '.scripts.dev // .scripts.start // .scripts.serve // "null"' package.json)
    if [ "$dev_script" != "null" ]; then
      discovered_command="npm run dev"
      doc_source="package.json scripts.dev"
    fi
  fi
  
  # If not found, prompt manually
  if [ -z "$discovered_command" ]; then
    echo "⚠️ Could not auto-discover dev command from package.json"
    echo "Please enter the command to start your application:"
    read -p "> " discovered_command
    doc_source="Manual user input"
  fi
fi

# Step 3: Extract port number (simple detection)
port=""

# From .env file
if [ -f ".env" ]; then
  port=$(grep "^PORT=" .env | cut -d= -f2)
fi

# Framework default fallback
if [ -z "$port" ]; then
  if [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
    port=3000
  elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
    port=5173
  elif [ -f "manage.py" ]; then
    port=8000
  else
    port=3000  # Default
  fi
fi

# Step 4: Prompt user for approval
echo ""
echo "ℹ️ Development Mode Command Discovered"
echo ""
echo "Command: $discovered_command"
echo "Source: $doc_source"
echo "Port: $port"
echo ""
echo "What would you like to do?"
echo ""
echo "1. Approve - Use this command as-is"
echo "2. Modify - Make changes to the command"
echo "3. Exit - Cancel and exit skill"
echo ""
read -p "Choose (1/2/3): " choice

case $choice in
  1)
    final_command="$discovered_command"
    echo "✅ Using command: $final_command"
    ;;
  2)
    echo ""
    echo "Enter the modified command:"
    read -p "> " user_modifications
    if [ -z "$user_modifications" ]; then
      echo "❌ No command provided. Exiting."
      exit 1
    fi
    final_command="$user_modifications"
    echo "✅ Using command: $final_command"
    ;;
  3)
    echo "❌ Command approval cancelled. Exiting skill."
    exit 1
    ;;
  *)
    echo "❌ Invalid choice. Please enter 1, 2, or 3."
    exit 1
    ;;
esac

# Step 5: Update config with approved command
command_hash=$(echo -n "$final_command" | sha256sum | awk '{print $1}')

# Update config with approved command and hash
python3 "$plugin_root/scripts/perf-config.py" set dev_environment.command_approved true
python3 "$plugin_root/scripts/perf-config.py" set metadata.dev_command_hash "$command_hash"

echo "✅ Dev command approved and saved to configuration"

# Step 6: Start application and verify with retry logic
echo ""
echo "ℹ️ Starting application: $final_command"
echo "⏳ Waiting for application to respond on port $port..."

# Start in background
$final_command &
app_pid=$!

# Verify with curl retry loop
max_retries=30
retry_delay=2

for i in $(seq 1 $max_retries); do
  if curl -s http://localhost:$port >/dev/null 2>&1; then
    echo "✅ Application is running on port $port"
    break
  fi
  
  if [ $i -lt $max_retries ]; then
    echo "   Attempt $i/$max_retries - waiting ${retry_delay}s..."
    sleep $retry_delay
  else
    echo ""
    echo "❌ Application failed to start after $((max_retries * retry_delay)) seconds"
    echo "Please check application logs for errors."
    kill $app_pid 2>/dev/null
    exit 1
  fi
done
```

**Change Detection:**

Dev commands are hashed using SHA-256 to detect changes:
- If command unchanged and approved: Skip prompt
- If command changed: Re-prompt for approval
- If never approved: Prompt for approval

**Error Handling:**

- If auto-discovery fails: Prompt manual input
- If user denies approval: Stop execution with actionable message
- If port verification fails: Stop execution with instructions

**Configuration Updates:**

After approval, update `.claude/performance-config.json`:
1. Development Environment table: Dev Command, Documentation Source, Port, Last Validated
2. Metadata: `dev_command_approved: true`, `dev_command_hash: "{sha256}"`

---

## Pattern 8: Code Intelligence Strategy (Serena-First with Grep Fallback)

**Purpose:** Ensure robust code analysis by always trying Serena MCP tools first, with automatic Grep fallback

**When to use:** **MANDATORY** for ALL code analysis operations including:
- Symbol lookup (finding functions, classes, handlers)
- File search and discovery
- Schema extraction (struct/class definitions)
- Reference counting (finding callers)
- AST/semantic analysis
- Any source code inspection or parsing

**Used by:**
- performance-baseline (Step 3.0 probe; Steps 3.1-A/B, 3.1.1-A/B, 3.5-A/B)
- performance-analyze-module (Step 6.9 probe; Steps 7.1-A/B, 7.2-A/B, 7.3–7.6)
- performance-implement-optimization (any code inspection during implementation)
- Any future skills that inspect source code

**Core Principle:**

```
GATE: One live Serena probe call at skill start sets serena_mode for the entire run.
  serena_mode = live           → Follow Path A steps (Serena-only, no grep)
  serena_mode = down           → Follow Path B steps (Grep, Serena probe errored)
  serena_mode = not-configured → Follow Path B steps (no Serena instance in config)
```

**Procedure:**

### Step 1: Live Serena Probe

Read `serena_instance` from the skill's config source (`performance-config.json` or `CLAUDE.md`):

```bash
serena_instance=$(python3 "$plugin_root/scripts/perf-config.py" get repositories.backend.serena_instance)
```

**If `serena_instance` is non-empty and not "—":**

Call `mcp__{serena_instance}__get_symbols_overview` with `relative_path="."`.

- **Response received (any result, including empty list):** `serena_mode = live`. Store the overview result for use in subsequent steps.
- **Error response received:** `serena_mode = down`. Record exact error string.

**If `serena_instance` is "—" or empty:** `serena_mode = not-configured`.

> The probe call doubles as useful data — the overview of the project root is the starting map
> for symbol discovery. Store and reuse it; do not discard it.

---

### Step 2-A: Code Analysis — Serena Path (`serena_mode = live`)

> **Grep and shell-based symbol discovery are not available in this path.**
> If an individual tool call errors on a specific file, mark that file
> `analysis_status: error` and continue with remaining files. Do not switch to grep.

Use the appropriate Serena tool for each operation:

| Operation | Tool | Key Parameters |
|---|---|---|
| All functions in a file | `find_symbol` | `name_path_pattern="/"`, `include_body=true`, `include_kinds=[12]`, `max_matches=100` |
| Callers of a function | `find_referencing_symbols` | `name_path=handler_name`, `relative_path=file` |
| File/module overview | `get_symbols_overview` | `relative_path=file`, `depth=1` |
| Named symbol search | `find_symbol` | `name_path_pattern=name`, `substring_matching=true` |
| Trace call to declaration | `find_declaration` | `relative_path=file`, `regex="obj\\.(method)\\("`, `include_body=true` |
| Find trait implementations | `find_implementations` | `name_path="Trait/method"`, `relative_path=file`, `include_info=true` |

**Batch over HTTP methods:** A single `find_symbol` call per file with `name_path_pattern="/"`
and `include_body=true` returns all handler functions including their route decorators
(`#[get]`, `#[post]`, etc.). Do not make separate calls per HTTP method.

Set `discovery_method = "Serena MCP"` and `confidence = "high"` on all results.

---

### Step 2-B: Code Analysis — Grep Path (`serena_mode = down | not-configured`)

> This path is followed only when Step 1 recorded `serena_mode = down` or `not-configured`.
> Document the reason in generated reports.

Use Grep and Read tools for symbol discovery. Apply framework-specific patterns defined in
each skill's discovery step.

Set `discovery_method = "Grep"` and `confidence = "medium"` on all results.

### Step 3: Document Method in Reports

Always document which analysis method was used in generated reports:
- Include "Analysis Method: Serena MCP (High Confidence)" or "Analysis Method: Grep (Fallback - Medium Confidence)"
- Add confidence level to anti-pattern detection tables
- If using Grep fallback, include limitations note

### Step 4: Confidence Levels

**High Confidence (Serena MCP):**
- Full AST/semantic analysis
- Accurate symbol resolution
- Cross-file reference tracking
- Type-aware field extraction
- Control flow analysis

**Medium Confidence (Grep - Good Patterns):**
- Pattern matching with context window
- Literal string search
- Line-proximity heuristics
- Best-effort parsing

**Low Confidence (Grep - Limitations):**
- Cannot detect destructuring (`const { field } = data`)
- Cannot track dynamic property access (`data[key]`)
- Cannot analyze control flow across functions
- May miss patterns split across many lines
- False positives on pattern matches in comments/strings

### Step 5: Error Handling Matrix

| `serena_mode` | Individual call result | Action | Confidence |
|---|---|---|---|
| `live` | Call succeeds | Use result, continue in Path A | High |
| `live` | Call errors on specific file | Mark file `analysis_status: error`, continue in Path A | High (partial) |
| `down` | — | Use Path B (Grep) throughout | Medium |
| `not-configured` | — | Use Path B (Grep) throughout | Medium |
| `live` + all files errored | All calls errored | Document in report as "Not Analyzed" | N/A |

---

## Pattern 9: Config Write Protection — REMOVED

Config writes use `perf-config.py set` / `set-json` which performs atomic writes via
`tempfile.NamedTemporaryFile` + `os.rename` (atomic on POSIX). No lockfile or mtime
checking required. For production CI environments, serialise performance skill runs at
the pipeline level.

---

## Pattern 10: API Profiling

**Purpose:** Execute accurate HTTP benchmarking of backend API endpoints with percentile calculation and cache effectiveness measurement.

**When to use:**
- Backend-only baseline capture (api-benchmark mode)
- Module-level dynamic performance testing
- Any scenario requiring accurate API latency percentiles (p50, p95, p99)

**Implementation:** `scripts/perf-benchmark.sh` (extracted script — replaces inline bash)

**Used by:**
- performance-baseline (Step 9.A — API Benchmark Mode for backend-only)
- performance-analyze-module (Step 7.7 — Dynamic Performance Testing)

**Prerequisites:**
- Backend service must be running on localhost
- `curl` and `jq` must be available (verified by script at startup)
- Test data manifest at `.claude/performance/test-data/manifest.json` (created by baseline)

**Execution:**

```bash
"$plugin_root/scripts/perf-benchmark.sh" \
  --port "$port" \
  --iterations "$iterations" \
  --manifest .claude/performance/test-data/manifest.json \
  --output .claude/performance/baselines/benchmark-results.json
```

The script handles all benchmarking logic: curl loops, percentile calculation (nearest-rank method),
cache effectiveness measurement, and JSON output via `jq`. See `perf-benchmark.sh --help` for details.

**Manifest schema:** `{ "endpoints": { "<path>": { "test_url": "<url>", "parameters": { "id": "<sample>" } } } }`

**Output schema (per endpoint):**
```json
{
  "test_url": "/api/v2/products",
  "iterations": 20,
  "samples_collected": 20,
  "p50_ms": 45,
  "p95_ms": 120,
  "p99_ms": 250,
  "mean_ms": 68,
  "first_request_ms": 850,
  "subsequent_mean_ms": 68,
  "cache_improvement_pct": "92.00",
  "cache_status": "Effective"
}
```

**Cache Effectiveness Classification:**
- **Effective:** > 50% improvement (cold vs warm mean)
- **Moderate:** 20-50% improvement
- **Minimal:** < 20% improvement
- **N/A:** First request failed or zero latency

**Error Handling:**
- Backend not running → Script exits with error (caller should check exit code)
- Missing `curl` or `jq` → Script exits with clear error message
- Individual endpoint failure → Logged, skipped, counted in `summary.failed_count`
- Authentication errors (401/403) → Endpoint marked failed, suggest `AUTH_DISABLED=true`

---

## Pattern 11: Jira Access Strategy

**Purpose:** Unified strategy for attempting Jira operations with MCP-first approach and REST API fallback

**When to use:** Before any Jira operation (issue creation, updates, transitions, comments)

**Used by:**
- performance-plan-optimization (Steps 8-10)
- performance-implement-optimization (Steps 2-4, 11-12)
- performance-verify-optimization (Steps 1, 4, 17-18)

**Procedure:**

**Step 1: Determine plugin root directory (do this once at skill initialization)**

**Apply:** [Pattern 0: Plugin Root Resolution](#pattern-0-plugin-root-resolution)

This resolves `$plugin_root` to the installed plugin directory (e.g., `~/.claude/plugins/cache/sdlc-plugins-local/sdlc-workflow/0.6.1/`)

**Step 2: For every Jira operation:**

1. **Attempt MCP first** (preferred method using Atlassian MCP server)
2. **If MCP fails, prompt user:**
   ```
   ❌ Atlassian MCP failed: {error_message}
   
   Would you like to use Jira REST API v3 fallback?
   
   Options:
   1. Yes - Use REST API (requires credentials)
   2. No - Skip this Jira operation
   3. Retry - I'll fix MCP configuration and retry
   
   Choose (1/2/3):
   ```

3. **If "1. Yes":** Check CLAUDE.md for existing REST API credentials, collect if missing, then use Python client
4. **If "2. No":** Skip the Jira operation and inform user
5. **If "3. Retry":** Retry MCP once

**REST API Equivalents:**

Common Jira operations with REST API fallback commands (using $plugin_root from Step 1):

- **Get issue:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" get_issue <id> --fields "*all"
  ```

- **Get user info:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" get_user_info
  ```

- **Assign issue:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" update_issue <id> --fields-json '{"assignee": {"id": "<accountId>"}}'
  ```

- **Transition issue:** 
  ```bash
  # First get transitions
  python3 "$plugin_root/scripts/jira-client.py" get_transitions <id>
  # Then transition (find ID for target status from above)
  python3 "$plugin_root/scripts/jira-client.py" transition_issue <id> --transition-id <id>
  ```

- **Update fields:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" update_issue <id> --fields-json '<json>'
  ```

- **Add comment:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" add_comment <id> --comment-md "<text>"
  ```

- **Create issue:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" create_issue --project <key> --issue-type <id> --summary "<text>" --description-md "<text>"
  ```

**Error handling:**

- If REST API also fails, report error and stop
- Always inform user which method was used (MCP or REST API)
- For missing credentials, prompt once and store in session for reuse

**Important:**

- REST API requires: `JIRA_SERVER_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` environment variables
- `$plugin_root` variable must be determined once at skill initialization (Step 1) and reused for all Jira operations
- The plugin path is typically `~/.claude/plugins/sdlc-workflow` but may vary by installation
- REST API fallback is only for Jira operations - never for code analysis or file operations

---

## Pattern 12: Call Chain Analysis Strategy

**Purpose:** Recursively trace function calls from an entry point (HTTP handler, service method, etc.) to detect performance anti-patterns hidden at any depth in the call graph — including service-layer N+1 queries, wasted computation, and unnecessary database operations.

**When to use:** After reading a handler/entry-point body, when the handler delegates to service methods, model builders, or utility functions that may contain queries, loops, or expensive operations.

**Used by:**
- performance-analyze-module (Steps 7.6.2-A, 7.6.2-B)
- Any future skills that need deep code inspection

**Core Principle:**

The pattern maintains three data structures during traversal:

1. **`call_graph`** — ordered list of `{caller, callee, file, depth}` edges representing the call tree
2. **`visited`** — set of `(file, symbol_name)` pairs to prevent infinite recursion on circular calls
3. **`query_ledger`** — list of `{description, depth, loop_multiplier, source_file, source_symbol}` entries for total query counting

**Configurable depth:** `analysis_chain_depth` (default: 3, read from Analysis Assumptions in `performance-config.json`).

---

### Step 1: Extract Call Sites from Body

Given a function body (from `find_symbol` with `include_body=true` or from the Read tool), extract method/function calls by matching these patterns:

| Call Pattern | Example | Resolution Strategy |
|---|---|---|
| `self.method_name(...)` | `self.fetch_sbom(id, &tx)` | Resolve within current impl block |
| `service.method_name(...)` | `fetcher.fetch_sbom_details(...)` | Determine service type from params, resolve in service file |
| `Type::associated_fn(...)` | `SbomDetails::from_entity(...)` | Resolve in type's impl block |
| `module::function(...)` | `utils::parse_id(...)` | Resolve in module directory |
| Direct function call | `decompress_async(bytes, ...)` | Resolve in current module or imports |

**Priority for tracing:** Focus on calls that are likely to contain database queries or expensive operations. Deprioritize calls to standard library functions, logging, serialization, or simple utility functions.

**Model builder heuristic:** Calls matching `Type::from_entity(...)`, `Type::from_row(...)`, `Type::from_model(...)`, or `Type::new(...)` are high-priority — these commonly contain hidden queries in Rust/Java/Python ORMs.

---

### Step 2: Resolve Each Call Site

**Path A — Serena (`serena_mode = live`):**

| Call Type | Serena Tool | Parameters |
|---|---|---|
| `self.method(...)` in same file | `find_declaration` | `relative_path=current_file`, `regex="self\\.(method)\\("`, `include_body=true` |
| `service.method(...)` typed param | `find_symbol` | `name_path_pattern="ServiceType/method"`, `relative_path=service_dir/`, `include_body=true`, `max_matches=1` |
| `Type::associated_fn(...)` | `find_symbol` | `name_path_pattern="Type/associated_fn"`, `include_body=true`, `max_matches=1` |
| Trait method call | `find_implementations` | `name_path="TraitName/method"`, `relative_path=file`, `include_info=true` |

If `find_symbol` returns no results, retry once with `substring_matching=true`. If still no result, record "Unresolved call: {call_expression}" and skip this branch.

**Path B — Grep (`serena_mode = down | not-configured`):**

1. Determine the target type from handler parameters (e.g., `fetcher: web::Data<SbomService>`)
2. Find the impl block: `grep -rn "impl ServiceType" modules/ --include="*.rs"`
3. Find the method: `grep -n "fn method_name" path/to/service.rs`
4. Read the method body with the Read tool (use line offset/limit from grep result)

Set `confidence = "medium"` at depth 0, `"low"` at depth > 1 for all Grep-path findings.

---

### Step 3: Recurse with Depth Limit and Cycle Detection

Before descending into a callee:

1. **Check depth:** `depth < analysis_chain_depth` (default 3)
2. **Check cycles:** `(callee_file, callee_name) not in visited`

**If either check fails:**
- Record the call edge in `call_graph` with annotation: `"⋯ Depth limit"` or `"⟳ Circular"`
- Do NOT descend — continue with remaining call sites at current depth

**If both checks pass:**
1. Add `(callee_file, callee_name)` to `visited`
2. Read the callee's body (Serena `find_symbol` with `include_body=true`, or Read tool)
3. Apply anti-pattern detection (Step 4)
4. Extract call sites from this callee's body → recurse back to Step 1 at `depth + 1`

---

### Step 4: Apply Anti-Pattern Checks at Each Depth

At every function body encountered during traversal, check for:

- **N+1 patterns:** Queries inside loops (same detection logic as Step 7.3 of performance-analyze-module)
- **Unused JOINs:** JOIN operations where joined table fields are never accessed (same as Step 7.6.1)
- **SELECT \* patterns:** ORM queries that fetch all columns without `.select_only()` (same as Step 7.6)
- **Missing caching:** Expensive operations without cache layer (same as Step 7.5)
- **Unnecessary computation:** Work done that is discarded by the caller (detected by comparing return type fields against caller's field access — see Step 7.6.3 in performance-analyze-module)
- **Conditional queries via lazy-load parameters (Memo/Option pattern):** When a function body
  contains a match/if on a `Memo<T>`, `Option<T>`, or similar lazy-load wrapper where one branch
  triggers a DB query and the other uses a pre-provided value:
  - Identify the parameter name and its type (e.g., `issuer: Memo<organization::Model>`)
  - Detect the branching pattern:
    ```
    Memo::Provided(value) => /* use value directly, no query */
    Memo::NotProvided => entity.find_related(...).one(tx).await?  // QUERY
    ```
  - Walk the `call_graph` upward to find ALL callers of this function
  - For each caller, check whether it passes the lazy variant (`Memo::NotProvided`, `None`) or the
    pre-loaded variant (`Memo::Provided(...)`, `Some(...)`)
  - If a caller passes the lazy variant, add the conditional query to `query_ledger` with
    `conditional: true` and `trigger` annotation (see format below)
  - Multiply by the caller's loop context if the caller is itself inside a loop
  - **Language-specific patterns:**
    - **Rust:** `Memo::NotProvided`, `Option::None`, `Lazy::new(|| ...)`
    - **Java:** `Optional.empty()`, `null` parameter, `@Lazy` annotation
    - **Python:** `None` default parameter, `lazy=True` flag
    - **Node:** `undefined` / `null` parameter, callback-based lazy loading

For each query or expensive operation found, add an entry to `query_ledger`:
```
{
  description: "human-readable query description",
  source_file: "relative/path/to/file.rs",
  source_line: 123,
  source_symbol: "SbomSummary::from_entity",
  depth: 2,
  query_type: "SELECT" | "COUNT" | "INSERT" | "UPDATE" | "DELETE",
  conditional: false,
  trigger: null,
  loop_context: {
    in_loop: true/false,
    loop_variable: "items",
    estimated_iterations: 25 or "N",
    loop_source: "paginated query with default limit 25"
  }
}
```

For conditional queries (Memo/Option pattern), set:
```
  conditional: true,
  trigger: "Memo::NotProvided passed by {caller_name} at {file}:{line}"
```

---

### Step 5: Calculate Query Totals

After traversal completes, process `query_ledger` to compute effective query counts:

```
For each query Q in query_ledger:
    effective_multiplier = 1
    
    Walk the call_graph from handler root to Q's source_symbol.
    For each edge on the path:
        If the caller contains a loop that iterates over the callee:
            effective_multiplier *= loop_iteration_count
    
    Also check Q's own loop_context:
    If Q.loop_context.in_loop:
        effective_multiplier *= Q.loop_context.estimated_iterations
    
    Q.effective_count = effective_multiplier

total_queries = sum(Q.effective_count for all Q in query_ledger)
estimated_db_latency = total_queries * analysis_db_latency_ms  # from Analysis Assumptions in performance-config.json, default 10ms
```

**Loop iteration estimation heuristics:**
- Collection from paginated query: use page_size (typically 20-25)
- Collection from unbounded query: use "N" and flag as "missing pagination"
- Fixed-size input (enum, config): use exact count
- Indeterminate: use "N" with note

**Post-traversal analysis:** After query totals are computed, the completed `query_ledger` can be
analyzed for inter-query duplication — see
[Step 7.6.5 in performance-analyze-module](../performance-analyze-module/SKILL.md#step-765--inter-query-duplication-detection)
for detection of shared CTEs and overlapping SQL logic across queries within the same handler chain.

---

### Error Handling

| Error | Action |
|---|---|
| `find_declaration` fails for a call site | Log it, skip that branch, continue with others |
| `find_symbol` returns no results | Retry once with `substring_matching=true`; if still empty, skip branch |
| Function body too large (> 500 lines) | Read body but limit recursion: extract only top-10 call sites by priority |
| Circular call detected | Record edge with "⟳ Circular" annotation, do not descend |
| Depth limit reached | Record edge with "⋯ Depth limit" annotation, do not descend |

---

## Usage Guidelines

### When to create a new pattern

Create a new pattern when:
- The same logic appears in 3+ skills
- The logic is complex enough to warrant standardization (>10 lines)
- The logic has error handling that should be consistent

### When NOT to create a pattern

Do not create a pattern when:
- The logic is skill-specific (unique to one skill)
- The logic is trivial (1-2 lines)
- The logic has high variability across skills

### Referencing patterns in skills

**Format:**

```markdown
## Step X – {Step Title}

**Apply:** [Common Pattern: {Pattern Name}](../performance/common-patterns.md#pattern-N-{pattern-slug})

**Specific actions for this skill:**
- Extract: {skill-specific detail}
- Validate: {skill-specific check}
- Store: {skill-specific variable}
```

**Example:**

```markdown
## Step 2 – Verify Performance Configuration Exists

**Apply:** [Common Pattern: Config Reading](../performance/common-patterns.md#pattern-1-config-reading)

**Specific actions for this skill:**
- Extract: Selected Workflow section
- Extract: Baseline Capture Settings
- Validate: Workflow has key screens defined
```

---

## Maintenance

**When updating a pattern:**

1. Update the pattern definition in this file
2. Verify all skills referencing the pattern still work correctly
3. Update pattern version history (if significant change)
4. Test end-to-end workflow with updated pattern

**Pattern versioning:**

## Pattern 13: Discovery Result Integrity

**Purpose:** Prevent silent data loss when tool output (grep, Serena, shell) is filtered, grouped, or summarized into an in-context table. Any post-processing that reduces the result set must be auditable.

**When to use:** Every time a discovery step produces results that feed into a downstream table, registry, or count — including endpoint discovery, symbol search, file listing, and anti-pattern detection.

**Used by:**
- performance-baseline (Steps 3.1-A, 3.1-B, 3.1.2)
- performance-analyze-module (Steps 6.1, 7.1-A, 7.1-B)

**The problem this prevents:** A raw grep returns N results. A secondary keyword filter (e.g., `grep -i "sbom\|advisory"`) is piped after it to narrow down to specific resources. Endpoints whose paths don't contain those keywords are silently dropped. The table is built from the filtered output, so downstream count checks (Step 3.1.2, Step 3.2.1) pass against the wrong baseline.

**Rules:**

1. **Record raw count immediately.** After every discovery tool call (grep, `find_symbol`, shell command), state the raw result count in your response before doing anything else with the output:

   > `▶ Raw result count: N items returned by {tool/command}`

2. **No secondary keyword filters on discovery output.** Never pipe discovery results through a second grep, `awk`, or any filter that selects a subset by content. If you need to categorize or narrow results, do so in-context when building the table — row by row — so that every raw result is either (a) added to the table or (b) explicitly excluded with a reason.

3. **Reconcile raw count against table rows.** After building the in-context table, compare:
   - `R` = raw result count from Rule 1
   - `T` = table row count

   **If R == T:** Proceed.

   **If R > T:** Some results were lost. List each missing result and either:
   - Add it to the table, OR
   - Document why it was excluded (duplicate, test-only, non-endpoint, etc.)

   **If R < T:** Results were duplicated. Deduplicate the table.

   Do not proceed to downstream steps until R and T are reconciled.

4. **Categorization belongs in the grouping step, not the discovery step.** Discovery produces the complete, unfiltered inventory. Grouping (e.g., Step 3.2) assigns categories. These are separate steps — do not collapse them.

**Anti-pattern examples (do NOT do these):**

```bash
# BAD: secondary filter silently drops non-matching endpoints
grep -rn '#\[get\|#\[post' src/ | grep -i "sbom\|advisory"

# BAD: awk/sed selecting only certain paths
grep -rn '@GetMapping' src/ | awk '/product|order/'
```

**Correct approach:**

```bash
# GOOD: unfiltered discovery
grep -rn '#\[get\|#\[post' src/
# Then: build table from ALL results in-context, categorize during grouping step
```

---

Patterns are not formally versioned. Breaking changes to patterns should be avoided. If a breaking change is necessary:
1. Create a new pattern (Pattern N+1)
2. Migrate skills gradually
3. Mark old pattern as deprecated
4. Remove old pattern after all skills migrated
