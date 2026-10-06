# Step 4 -- Root Cause Analysis

## Root Cause

The plan-feature skill's convention conformance analysis extracts `CONVENTIONS.md` section headings using `line[3:]` without stripping trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted section name retains those spaces (`"Migration Patterns  "`). The subsequent convention-aware task enrichment step performs an exact-match dictionary lookup using the clean convention name (`"Migration Patterns"`), which fails against the whitespace-padded key. The convention is silently dropped from the generated task description with no warning or error.

## Affected Files

| File | Symbol/Location | Issue |
|------|-----------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention lookup loop (`line[3:]`) | Heading extraction does not call `.strip()` on the extracted section name |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Task enrichment (`convention_name in discovered_conventions`) | Exact-match lookup fails for whitespace-padded keys; no fallback or warning |

## Suggested Approach

1. **Primary fix**: Add `.strip()` to the heading extraction line so that `section_name = line[3:].strip()` normalizes trailing whitespace before storing in the conventions dictionary.
2. **Defensive improvement**: Also consider stripping the lookup key (`convention_name.strip()`) at the matching site, for defense in depth.
3. **Observability**: Add a warning log when a convention section from `CONVENTIONS.md` is not matched during task enrichment, so future mismatches are visible rather than silent.

## Reproducer Strategy

1. Create a test `CONVENTIONS.md` fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  ` with two trailing spaces).
2. Run the plan-feature convention lookup against this fixture.
3. Assert that the convention IS matched and included in the generated task's Implementation Notes, despite the trailing whitespace.
4. Before the fix, the assertion should fail (convention silently dropped). After the fix, the assertion should pass (convention correctly included).

## How to Verify

- The reproducer test above validates the fix.
- Additionally, run existing plan-feature evals to ensure no regression in standard (no trailing whitespace) convention handling.

---

This analysis would be posted as a comment on ACME-500 with ADF contentFormat, including the Comment Footnote.
