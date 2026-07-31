# Step 2 & 3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction Method: Code-Path Tracing

This bug involves a skill's convention conformance analysis (a documentation/template processing issue), so direct reproduction via runnable commands is not applicable. Code-path tracing is used instead.

### Entry Point

The entry point is the `/plan-feature ACME-100` skill invocation, which triggers convention conformance analysis as part of task generation.

### Trace Findings

**Trace path**: `/plan-feature` invocation -> CONVENTIONS.md reading -> heading extraction -> convention name lookup -> task enrichment

1. **CONVENTIONS.md parsing** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   The skill reads CONVENTIONS.md line by line, looking for lines starting with `## `:
   ```python
   for line in conventions_content.split('\n'):
       if line.startswith('## '):
           section_name = line[3:]  # Extracts heading text after "## "
           conventions[section_name] = current_section_content
   ```
   When the heading line is `## Migration Patterns  \n`, `line[3:]` produces `"Migration Patterns  "` (with trailing spaces). No `.strip()` or `.rstrip()` is applied.

2. **Convention-aware task enrichment** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):
   The task enrichment step looks up conventions by name using exact string matching:
   ```python
   if convention_name in discovered_conventions:
       notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
   ```
   The lookup uses the clean name `"Migration Patterns"` but the dictionary key is `"Migration Patterns  "` (with trailing spaces). The exact match fails silently -- no warning, no error, no fallback.

3. **Divergence point**: The behavior diverges from expected at the heading extraction step. The `line[3:]` call preserves trailing whitespace, which then propagates through the dictionary key, causing all downstream lookups to fail for any heading with trailing whitespace.

## Step 3 -- Codebase Investigation

### Target Repository

- **Repository**: acme-backend
- **Component**: sdlc-workflow (from bug metadata)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected Files and Symbols

| File | Symbol/Section | Role |
|------|---------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis | Contains the heading extraction logic with the `line[3:]` bug |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Contains the exact-match lookup that fails due to trailing whitespace |

### Existing Test Coverage

| Test File | Coverage |
|-----------|----------|
| `evals/plan-feature/files/conventions-mock.md` | Existing eval fixture for plan-feature conventions -- does NOT include trailing whitespace on headings. This edge case is not covered by current evals. |

### CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to reference in the generated task's Implementation Notes.

### Persistence-Impact Analysis

**No persistence boundary found.** The output of the convention conformance analysis is the generated task description content (specifically the Implementation Notes section). This content is:
- Computed at task generation time (when `/plan-feature` runs)
- Written to Jira as a task description via the Jira API
- Not persisted to a database table within the application

The bug affects the content of generated Jira tasks, but this is computed output, not ingested/persisted data within the application's data model. No data migration is needed. Fixing the heading extraction logic will correct all future task generations.

### Patterns for the Fix

The fix requires adding whitespace stripping to the heading extraction. The correct pattern:
```python
section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

This is a single-character-class change at a single location. The fix should also consider adding a warning log when trailing whitespace is detected and stripped, to aid debugging similar issues in the future.
