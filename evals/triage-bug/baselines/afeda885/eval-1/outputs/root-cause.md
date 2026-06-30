# Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention heading extraction uses `line[3:]` to extract the section name from `## `-prefixed heading lines in `CONVENTIONS.md`. This slicing operation does not strip trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted key becomes `"Migration Patterns  "` (with trailing spaces). The subsequent exact-match lookup against the normalized convention name `"Migration Patterns"` fails, causing the convention to be silently dropped from the generated task description.

## Affected Files

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention conformance analysis section, heading extraction logic (`line[3:]` without `.strip()`)
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment section (exact-match lookup with no fallback or warning)

## Suggested Approach

1. **Primary fix**: Change the heading extraction from `line[3:]` to `line[3:].strip()` to normalize section names by removing trailing whitespace.
2. **Secondary improvement**: Add a warning log when a convention referenced during task enrichment is not found in the discovered conventions dictionary, to prevent silent failures for other edge cases.
3. **Test coverage**: Add an eval fixture with trailing whitespace on convention headings to `evals/plan-feature/files/conventions-mock.md` to prevent regression.

## Reproducer Strategy

1. Create a `CONVENTIONS.md` fixture with trailing whitespace on at least one heading line (e.g., `## Migration Patterns  ` with two trailing spaces).
2. Run the plan-feature convention extraction logic against this fixture.
3. Assert that the extracted section name equals `"Migration Patterns"` (without trailing whitespace).
4. Assert that the generated task's Implementation Notes include the convention reference: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
