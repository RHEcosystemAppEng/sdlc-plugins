# Step 4 -- Root Cause Analysis

## Root Cause

The dark mode preference fails to persist because the preference key lookup relies
on exact string matching against section headings extracted from a configuration
file. The heading extraction logic (`line[3:]`) does not strip trailing whitespace
from parsed heading text. When headings contain trailing spaces (e.g.,
`"Dark Mode  "` instead of `"Dark Mode"`), the subsequent dictionary lookup fails
silently, causing the preference to be ignored on reload.

Specifically:

1. **What is broken**: The convention/settings heading extraction in
   `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` produces section names
   with trailing whitespace when the source file contains trailing spaces on
   heading lines.

2. **Why it is broken**: The extraction code `section_name = line[3:]` does not
   call `.strip()` on the result. This means any trailing whitespace on the heading
   line becomes part of the key used for dictionary lookups.

3. **Where it is broken**:
   - `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention heading
     extraction (the `line[3:]` expression)
   - `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware
     task enrichment (the `convention_name in discovered_conventions` check)

4. **How to verify the fix**: A reproducer test should:
   - Create a conventions file with trailing whitespace on at least one heading
   - Run the heading extraction logic
   - Assert that the extracted section name matches the expected value without
     trailing whitespace
   - Assert that the convention-aware task enrichment successfully matches the
     heading

## Affected Files

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- heading extraction and
  convention matching logic
- `evals/plan-feature/files/conventions-mock.md` -- test fixture lacking trailing
  whitespace edge case

## Suggested Approach

Apply `.strip()` to the extracted heading text at the point of extraction:

```python
section_name = line[3:].strip()
```

This normalizes heading names at the source, ensuring all downstream lookups
succeed regardless of trailing whitespace in the source file.

## Reproducer Strategy

1. Add a conventions mock file (or modify the existing one) that includes headings
   with trailing whitespace (e.g., `## Migration Patterns  ` with trailing spaces).
2. Run the plan-feature convention extraction against this fixture.
3. Assert that the heading is extracted as `"Migration Patterns"` (without trailing
   spaces).
4. Assert that convention-aware task enrichment finds and applies the convention.

## Jira Comment

The following root cause analysis would be posted as a comment on ACME-511:

**Root Cause**: Heading extraction in the plan-feature skill does not strip
trailing whitespace from parsed section names. When convention headings have
trailing spaces, exact-match lookups fail silently, causing preferences/conventions
to be ignored.

**Affected Files**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` (heading extraction + task enrichment)

**Suggested Approach**: Add `.strip()` to `line[3:]` in the heading extraction
loop to normalize section names at parse time.

**Reproducer Strategy**: Create a test fixture with trailing whitespace on
headings and assert that extraction produces clean names and lookups succeed.
