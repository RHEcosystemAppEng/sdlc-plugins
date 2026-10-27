# Steps 2-3 -- Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Code-path tracing

This bug involves a skill's convention parsing logic and cannot be directly reproduced via CLI command. Instead, we trace through the code paths described in the repository context.

#### Entry point

The entry point is the `/plan-feature` skill invocation (Step to Reproduce #2). When plan-feature runs, it performs a convention conformance analysis by reading `CONVENTIONS.md` and extracting section headings.

#### Trace through convention lookup

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The convention lookup iterates over lines of `CONVENTIONS.md` and extracts headings:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Key finding**: `line[3:]` slices the string from position 3 to the end, but does **not** strip trailing whitespace. When the heading line is `## Migration Patterns  \n` (with trailing spaces), the extracted `section_name` becomes `"Migration Patterns  "` (with trailing spaces included).

#### Trace through convention-aware task enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

The task enrichment step matches conventions by exact string comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The `convention_name` used in the lookup (e.g., `"Migration Patterns"`) does not have trailing whitespace, but the key stored in `discovered_conventions` does (e.g., `"Migration Patterns  "`). The `in` check fails because `"Migration Patterns" != "Migration Patterns  "`.

#### Divergence point

The actual behavior diverges from expected behavior at the heading extraction step. The `line[3:]` slice preserves trailing whitespace from the source file, creating a key mismatch in the subsequent dictionary lookup. No warning or error is emitted when the lookup fails -- the convention is silently skipped.

#### Reproduction outcome

**Confirmed via code-path trace.** The bug is reproducible whenever a `CONVENTIONS.md` heading line contains trailing whitespace characters.

## Step 3 -- Codebase Investigation

### Target repository

- **Component**: sdlc-workflow
- **Repository**: acme-backend (from Repository Registry)
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

### Affected files and symbols

| File | Symbol / Location | Role |
|------|-------------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention lookup loop | Heading extraction with `line[3:]` -- the defect location |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment | Exact-match lookup that fails due to trailing whitespace |

### Existing test coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does **not** include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions apply to the fix task itself.

### Persistence-impact analysis

The convention lookup output (the `conventions` dictionary and the generated task description notes) is **not** persisted to a database at ingestion time. The convention matching happens during task generation and the output is written directly to a Jira task description via the API. This is a computed-at-generation-time value.

**Result**: No persistence boundary found. No data migration is needed. The code fix alone will correct all future task generation behavior.

### Root cause summary for Step 4

The root cause is the missing `.strip()` call on `line[3:]` in the convention heading extraction. The fix is to strip trailing whitespace from the extracted heading text so that exact-match lookups succeed regardless of trailing whitespace in the source `CONVENTIONS.md` file.
