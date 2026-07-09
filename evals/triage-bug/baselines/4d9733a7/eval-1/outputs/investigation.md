# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction approach

The Steps to Reproduce describe a skill invocation (`/plan-feature ACME-100`) rather than a
runnable CLI command, so direct reproduction is not possible. Code-path tracing is used instead.

### Code-path trace

**Entry point**: The plan-feature skill's convention conformance analysis, which reads
`CONVENTIONS.md` and extracts heading-based sections for task enrichment.

**Trace through convention extraction:**

In `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, the convention lookup logic iterates
over lines in `CONVENTIONS.md` and extracts section headings:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The extraction `line[3:]` takes everything after the `## ` prefix but does **not** strip
trailing whitespace. When a heading line has trailing spaces (e.g., `## Migration Patterns  \n`),
the extracted key becomes `"Migration Patterns  "` (with trailing spaces).

**Trace through convention matching:**

The task enrichment step performs an exact match on the convention name:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The lookup key `"Migration Patterns"` does not match the stored key `"Migration Patterns  "`,
so the convention is silently skipped. No warning or error is emitted for unmatched conventions.

**Divergence point**: The behavior diverges at the `line[3:]` extraction -- the heading text
retains trailing whitespace, causing the downstream exact-match lookup to fail.

### Reproduction outcome

**Confirmed via trace**: The bug is confirmed through code-path analysis. The `line[3:]`
extraction does not strip trailing whitespace, and the downstream exact-match comparison
fails when headings have trailing spaces.

## Step 3 -- Codebase Investigation

### Target repository

- **Repository**: acme-backend (based on Component: sdlc-workflow and Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Note: Code Intelligence section states "No Serena MCP servers are configured. Code intelligence
is not available." Fallback to Read/Grep/Glob is used.

### Affected files and symbols

| File | Symbol / Location | Role |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention extraction loop (`line[3:]`) | Defect location -- heading extraction without `.strip()` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Failure point -- exact-match lookup fails due to trailing whitespace in key |

### Existing test coverage

- **Existing fixture**: `evals/plan-feature/files/conventions-mock.md` -- this fixture does NOT
  include trailing whitespace on headings, so the edge case is not covered by current evals.
- **Gap**: No test case exercises heading lines with trailing whitespace in `CONVENTIONS.md`.

### CONVENTIONS.md lookup

The repository (`acme-backend`) does not have a `CONVENTIONS.md` file at its root.
No additional conventions apply to the fix task.

### Reuse candidates

No existing utility or helper for whitespace-safe heading extraction was found.
The fix will need to add `.strip()` to the extraction logic.

### Investigation summary

- **Single root cause**: The bug has a single root cause (missing `.strip()` on heading
  extraction), so the Decomposition Guard (Step 6) does not apply.
- **Affected code path**: Convention extraction -> convention matching -> task enrichment.
- **Fix scope**: Add `.strip()` to `line[3:]` in the convention extraction loop, and
  optionally add a warning when a convention heading has trailing whitespace.
