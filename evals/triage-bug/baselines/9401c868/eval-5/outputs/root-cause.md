# Step 4 -- Root Cause Analysis: ACME-511

## Root Cause Determination

### What is broken

The convention heading extraction in the plan-feature skill does not strip trailing
whitespace from parsed `CONVENTIONS.md` section headings. When a heading line contains
trailing spaces (e.g., `## Migration Patterns  `), the extracted section name retains
those spaces, causing downstream exact-match lookups to fail silently.

In the context of the reported bug (dark mode toggle not persisting), the preference
persistence mechanism relies on convention-aware task enrichment to apply the correct
persistence pattern. When convention matching fails due to trailing whitespace in
heading names, the persistence-related convention guidance is silently dropped from
the generated task, resulting in the preference not being persisted across browser
sessions.

### Why it is broken

The heading extraction code at `line[3:]` in the convention parsing logic extracts
everything after the `## ` prefix without calling `.strip()` on the result. This
is a missing input normalization step. The downstream match uses Python's `in`
operator for dictionary key lookup, which performs exact string comparison and does
not tolerate trailing whitespace differences.

### Where it is broken

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
- **Symbol**: Convention heading extraction block (the `for line in conventions_content.split('\n')` loop)
- **Specific line**: `section_name = line[3:]` -- missing `.strip()` call

### How to verify the fix

A reproducer test should:

1. Create a mock `CONVENTIONS.md` with trailing whitespace on at least one heading
   (e.g., `## Migration Patterns  ` with trailing spaces).
2. Run the convention parsing logic on this input.
3. Assert that the extracted section name matches the expected name WITHOUT trailing
   whitespace (i.e., `"Migration Patterns"`, not `"Migration Patterns  "`).
4. Assert that the convention-aware task enrichment lookup succeeds for the section.

## Root Cause Comment (would be posted to ACME-511)

**Root Cause**: The convention heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses `line[3:]` without stripping trailing whitespace. When CONVENTIONS.md headings contain trailing spaces, the extracted section names fail exact-match lookups in the task enrichment step, silently dropping convention-aware guidance.

**Affected Files**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention heading extraction loop

**Suggested Approach**: Add `.strip()` to the heading extraction line: `section_name = line[3:].strip()`. This normalizes the heading text and ensures downstream dictionary lookups succeed regardless of trailing whitespace in the source file.

**Reproducer Strategy**: Write a test that parses a CONVENTIONS.md fixture containing headings with trailing whitespace and asserts that the extracted section names match the expected trimmed values, and that convention-aware enrichment lookups succeed.
