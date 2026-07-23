# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Code Intelligence Note

Per CLAUDE.md Code Intelligence section: "No Serena MCP servers are configured. Code intelligence is not available." Fallback to Read/Grep/Glob for investigation.

## Investigation Findings

### Finding 1: Convention Heading Extraction (Root Cause Location)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

The plan-feature skill reads `CONVENTIONS.md` headings using this logic:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The heading extraction at `line[3:]` does NOT strip trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with two trailing spaces). This mismatches the expected `"Migration Patterns"` during lookup.

### Finding 2: Convention-Aware Task Enrichment (Failure Point)

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

The task enrichment step matches conventions by exact section name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This exact-match comparison fails when `convention_name` is `"Migration Patterns"` but the dictionary key is `"Migration Patterns  "` (with trailing spaces). The convention is silently skipped with no warning or error logged.

### Finding 3: Missing Test Coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is entirely uncovered by current evals and tests.

### Finding 4: No CONVENTIONS.md in Repository Root

The repository does not have a `CONVENTIONS.md` at its root. This means there are no project-level conventions to reference in the generated task's Implementation Notes.

## Affected Files and Symbols

| File | Symbol/Section | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention conformance analysis -- heading extraction (`line[3:]`) | Root cause: missing `.strip()` on extracted heading name |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment -- `convention_name in discovered_conventions` | Failure point: exact match fails due to trailing whitespace |
| `evals/plan-feature/files/conventions-mock.md` | Eval fixture | Missing coverage: no trailing whitespace test case |

## Existing Test Patterns

The eval fixture `evals/plan-feature/files/conventions-mock.md` provides the pattern for testing convention conformance. A reproducer test should create a variant of this fixture with trailing whitespace on headings to exercise the edge case.

## Reuse Candidates

- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture; can be extended or duplicated with trailing whitespace variant for the reproducer test.
