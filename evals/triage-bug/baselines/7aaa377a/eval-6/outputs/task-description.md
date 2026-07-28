# Step 5 – Generated Task Description for ACME-500

*This is the task description that would be submitted via `jira.create_issue()`. The task would
be linked to ACME-500 using the "Blocks" link type (Task blocks Bug), with the `ai-generated-jira`
label applied.*

---

## Repository
acme-backend

## Target Branch
main

## Description

Fix the `plan-feature` skill's convention conformance analysis to correctly handle
`CONVENTIONS.md` headings that contain trailing whitespace. Currently, heading lines such as
`## Migration Patterns  ` (with trailing spaces) are stored with the whitespace embedded in
the section name, causing exact-match lookups to fail silently. The resulting task descriptions
omit conventions that should have been included, with no warning to the user.

This fix strips trailing whitespace from extracted heading names at the point of extraction,
ensuring that convention sections are reliably matched regardless of whitespace artifacts in
the source file. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — Change `section_name = line[3:]` to `section_name = line[3:].rstrip()` in the convention conformance analysis heading extraction loop

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — New eval fixture mirroring `conventions-mock.md` but with trailing spaces on all `## …` heading lines, used as the reproducer test input

## Implementation Notes

**Bug**: Fixes ACME-500 — plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace.

**Defect site** (`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`):

The convention conformance analysis loop currently reads:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]   # BUG: retains trailing whitespace
        conventions[section_name] = current_section_content
```

The fix is:

```python
        section_name = line[3:].rstrip()   # FIXED: trailing whitespace stripped
```

Use `.rstrip()` (right-strip only) rather than `.strip()`. Leading spaces after `"## "` could
in principle be intentional indentation; trailing spaces in Markdown headings are universally
noise. This single-character change eliminates the root cause.

**Why the secondary location (enrichment match) needs no change**:

The task enrichment lookup `if convention_name in discovered_conventions:` works correctly
once the keys in `discovered_conventions` are clean. No changes are needed there.

**Reproducer test construction** (for `evals/plan-feature/files/conventions-trailing-whitespace-mock.md`):

1. Copy the structure of the existing `evals/plan-feature/files/conventions-mock.md` fixture.
2. Add trailing spaces (two spaces `  `) to every `## …` section heading line. Example:
   ```markdown
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
3. The fixture must include at least the `## Migration Patterns` section with trailing spaces,
   since that is the exact scenario described in ACME-500.
4. The test should confirm:
   - **Before fix**: `"Migration Patterns"` key is NOT found in `discovered_conventions`
     (trailing-whitespace key mismatch).
   - **After fix**: `"Migration Patterns"` key IS found in `discovered_conventions`, and the
     generated task's Implementation Notes include the string
     `"Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns."`.

**Existing test pattern to follow**: `evals/plan-feature/files/conventions-mock.md` — use the
same fixture format, field structure, and assertion style. The new fixture is a targeted variant
that isolates the trailing-whitespace edge case.

**No data migration needed**: the convention lookup is computed fresh on every skill invocation
from the current `CONVENTIONS.md` content. No values are persisted to a database. Fixing the
extraction logic corrects all future invocations immediately.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing fixture format to copy as the baseline for the new trailing-whitespace fixture; ensures the new test follows established eval patterns

## Acceptance Criteria
- [ ] **Reproducer (must fail before fix, pass after)**: Running the convention conformance analysis against `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` (which has `## Migration Patterns  ` with trailing spaces) produces a generated task whose Implementation Notes include `"Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns."`
- [ ] The heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses `.rstrip()` on the extracted section name so that trailing whitespace is removed before the name is stored in `discovered_conventions`
- [ ] A `CONVENTIONS.md` with headings that have trailing spaces is processed identically to one with clean headings — no conventions are silently dropped
- [ ] No regression in existing plan-feature evals (including those using `evals/plan-feature/files/conventions-mock.md`)

## Test Requirements
- [ ] **Reproducer test** (first): Create `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with `## Migration Patterns  ` (two trailing spaces); assert that after the fix the generated task Implementation Notes reference the Migration Patterns convention. This test must fail on the unfixed code to confirm it reproduces the bug.
- [ ] **Regression test**: Run the existing plan-feature eval suite against `evals/plan-feature/files/conventions-mock.md` and verify all tests continue to pass after the `.rstrip()` change is applied.

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**:
  1. Create `CONVENTIONS.md` with `## Migration Patterns  ` (trailing spaces on the heading line) and `Add Index::create() for all FK columns.` as the section body.
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
  3. Inspect the generated task's Implementation Notes — the Migration Patterns convention is absent.
- **Expected Result**: The generated task's Implementation Notes include `"Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns."`
- **Actual Result**: The Implementation Notes do not reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: `plan-feature`'s convention heading extraction uses `line[3:]` without `.rstrip()`. Headings with trailing whitespace produce dictionary keys with embedded spaces (e.g., `"Migration Patterns  "`), causing exact-match lookups against clean expected names (e.g., `"Migration Patterns"`) to fail silently.
