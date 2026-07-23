# Step 2 & 3 -- Reproduction Trace and Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction Method: Code-Path Tracing

The Steps to Reproduce reference running `/plan-feature ACME-100`, which is a skill invocation rather than a directly runnable command. This is a skill/behavior bug, so code-path tracing is the appropriate reproduction method.

### Trace Findings

**Entry point**: The `/plan-feature` skill invocation triggers the convention conformance analysis, which reads `CONVENTIONS.md` and matches section headings against expected convention names.

**Divergence point identified**: The heading extraction code does not strip trailing whitespace from heading lines. When a heading line contains trailing spaces (e.g., `## Migration Patterns  \n`), the extracted section name retains those spaces (`"Migration Patterns  "` instead of `"Migration Patterns"`). The subsequent exact-match comparison against the canonical convention name `"Migration Patterns"` fails, causing the convention to be silently skipped with no warning or error output.

**Reproduction outcome**: Confirmed via code-path tracing. The bug is deterministic: any `CONVENTIONS.md` heading with trailing whitespace will cause the corresponding convention to be silently dropped.

## Step 3 -- Codebase Investigation

### Target Repository

- **Repository**: acme-backend
- **Component**: sdlc-workflow (from bug's Component field)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Code Intelligence Note

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available." Falling back to Read/Grep/Glob tools.

### Affected Files and Symbols

#### 1. Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Defect**: `line[3:]` extracts the heading text starting after the `## ` prefix but does NOT call `.strip()` or `.rstrip()` to remove trailing whitespace. If the source line is `## Migration Patterns  \n`, the resulting `section_name` is `"Migration Patterns  "` (with trailing spaces).

#### 2. Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Defect**: The `in` lookup uses exact string matching against dictionary keys. Since the key was stored with trailing whitespace (`"Migration Patterns  "`), a lookup for `"Migration Patterns"` fails. No fallback or fuzzy matching is attempted, and no warning is logged.

#### 3. Existing Test Coverage Gap

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case has no test coverage.

### CONVENTIONS.md Lookup

The repository (acme-backend) does not have a `CONVENTIONS.md` file at its root. No conventions to incorporate into the task's Implementation Notes.

### Summary of Investigation Findings

| Finding | File | Detail |
|---------|------|--------|
| Heading extraction lacks `.strip()` | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | `line[3:]` preserves trailing whitespace |
| Convention match uses exact lookup | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | `convention_name in discovered_conventions` fails on whitespace mismatch |
| No silent-drop warning | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | No logging when a convention is expected but not found |
| No test coverage for edge case | `evals/plan-feature/files/conventions-mock.md` | Existing fixtures lack trailing whitespace in headings |
