# Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention conformance analysis extracts `CONVENTIONS.md` section headings using `line[3:]`, which captures all characters after the `## ` prefix without stripping trailing whitespace. When a heading line ends with trailing spaces (e.g., `## Migration Patterns  `), the extracted section name retains those spaces (`"Migration Patterns  "`). The subsequent convention lookup performs an exact string match against the canonical section name (`"Migration Patterns"`), which fails due to the trailing whitespace mismatch. The convention is silently dropped with no warning.

## Affected Files

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention conformance analysis section
  - Heading extraction: `section_name = line[3:]` (missing `.strip()`)
  - Convention matching: exact-match lookup against extracted keys

## Suggested Approach

1. Apply `.strip()` to the heading extraction to normalize whitespace:
   ```python
   section_name = line[3:].strip()
   ```
2. Add a warning log when a convention section name contains leading or trailing whitespace in the source `CONVENTIONS.md`, to help users identify formatting issues.
3. Add a reproducer test that uses a `CONVENTIONS.md` fixture with trailing whitespace on a heading line, confirming the convention is correctly matched and included in the generated task description.

## Reproducer Strategy

1. Create a test fixture `CONVENTIONS.md` with trailing whitespace on at least one heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run the plan-feature convention lookup against this fixture.
3. Assert that the convention keyed as `"Migration Patterns"` is present in the discovered conventions dictionary.
4. Assert that the generated task description includes the expected Implementation Notes reference:
   `Per CONVENTIONS.md Section Migration Patterns: add Index::create() for all FK columns.`
