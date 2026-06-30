# Codebase Investigation: ACME-500

## Step 2 -- Reproduce/Trace

### Reproduction Scenario

Following the Steps to Reproduce from the bug report:

1. A `CONVENTIONS.md` file exists with trailing whitespace on a heading line:
   ```
   ## Migration Patterns  \n
   Add Index::create() for all FK columns.
   ```
   Note the two trailing spaces after "Migration Patterns" before the newline.

2. When `/plan-feature ACME-100` runs, the plan-feature skill reads `CONVENTIONS.md` and attempts to extract convention sections by heading name.

3. The generated task's Implementation Notes omit the "Migration Patterns" convention entirely, with no warning or error.

### Trace Through Code

The convention extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses the following code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

When the heading line is `## Migration Patterns  ` (with trailing spaces):
- `line.startswith('## ')` evaluates to `True` -- the line is correctly identified as a heading
- `line[3:]` extracts `"Migration Patterns  "` (with trailing spaces preserved)
- The key stored in the `conventions` dictionary is `"Migration Patterns  "` (with trailing whitespace)

Later, the task enrichment step performs an exact match:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

The lookup key `convention_name` is `"Migration Patterns"` (without trailing spaces), so the dictionary lookup against `"Migration Patterns  "` fails. The convention is silently skipped.

## Step 3 -- Codebase Investigation

### Affected File

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Location**: Convention conformance analysis section -- heading extraction logic

**Root Issue**: `line[3:]` does not call `.strip()` or `.rstrip()` to remove trailing whitespace from the extracted heading text.

### Why No Warning

There is no fallback or warning mechanism when a convention referenced in the feature analysis is not found in the `discovered_conventions` dictionary. The `if convention_name in discovered_conventions` check silently skips unmatched conventions.

### Test Coverage Gap

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does NOT include trailing whitespace on headings. This means the edge case is not covered by current evals, and the bug could not have been caught by existing tests.

### Fix Approach

The fix is straightforward: add `.strip()` to the heading extraction:

```python
section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

This normalizes the section name so that exact-match lookups succeed regardless of trailing whitespace in the source file.

A secondary improvement would be to add a warning when a convention referenced during task enrichment is not found in `discovered_conventions`, to prevent silent failures in the future.
