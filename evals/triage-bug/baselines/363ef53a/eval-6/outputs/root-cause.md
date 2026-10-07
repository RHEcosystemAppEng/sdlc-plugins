# Root Cause Analysis -- ACME-500

## Root Cause

The plan-feature skill's convention heading parser extracts section names from CONVENTIONS.md using `line[3:]` without stripping trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted section name includes those spaces (`"Migration Patterns  "`). Later, when the task enrichment step performs an exact-match lookup against the expected convention name (`"Migration Patterns"`), the match fails because the strings differ by trailing whitespace. The convention is silently dropped from the generated task description with no warning or error logged.

## Fix Approach

1. **Primary fix**: Strip trailing whitespace from the extracted heading text during parsing. Change `line[3:]` to `line[3:].strip()` (or `.rstrip()`) so that trailing whitespace on CONVENTIONS.md heading lines is normalized before storing in the conventions dictionary.

2. **Defensive improvement**: Add a warning log when a convention that was expected to match is not found in the discovered conventions dictionary. This would make similar silent-failure bugs easier to detect in the future.

3. **Test coverage**: Add an eval fixture (or update the existing `evals/plan-feature/files/conventions-mock.md`) that includes trailing whitespace on convention headings to prevent regression.

## Impact

- **Severity**: Medium -- conventions are silently dropped, leading to incomplete task descriptions that miss required implementation guidance. This can result in implementations that violate project conventions without the implementer being aware.
- **Scope**: Affects any project using CONVENTIONS.md where heading lines have trailing whitespace, which is common in hand-edited Markdown files.
