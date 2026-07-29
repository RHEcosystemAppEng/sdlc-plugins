# Step 4 -- Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention conformance analysis extracts CONVENTIONS.md section headings using `line[3:]` without stripping trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted section name retains those spaces (`"Migration Patterns  "`). The subsequent exact-match lookup against expected convention names (which do not have trailing spaces) fails silently, causing the convention to be omitted from the generated task description with no warning or error.

## What Is Broken

The string extraction logic in the convention heading parser. The expression `line[3:]` slices the heading prefix `## ` but preserves any trailing whitespace characters on the line. This produces dictionary keys that do not match the canonical (trimmed) convention names used during task enrichment.

## Why It Is Broken

The code assumes that heading lines in CONVENTIONS.md have no trailing whitespace. This assumption is fragile because:
1. Many text editors silently add or preserve trailing whitespace.
2. Copy-paste operations frequently introduce trailing spaces.
3. Not all repositories enforce trailing whitespace linting on Markdown files.

The lack of a `.strip()` call (or equivalent whitespace normalization) on the extracted heading text makes the parser sensitive to formatting variations that have no semantic meaning.

## Where It Is Broken

| File | Location | Defect |
|---|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction: `section_name = line[3:]` | Missing `.strip()` on extracted heading text |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment: `if convention_name in discovered_conventions` | No fuzzy/normalized matching, no warning on miss |

## How to Verify the Fix (Reproducer Strategy)

A reproducer test should:

1. **Setup:** Create a CONVENTIONS.md fixture with trailing whitespace on at least one heading line (e.g., `## Migration Patterns  ` with two trailing spaces).
2. **Exercise:** Run the convention heading extraction logic against this fixture.
3. **Assert (before fix):** The convention keyed by `"Migration Patterns"` is NOT found in the extracted conventions dictionary -- confirming the bug exists.
4. **Assert (after fix):** The convention keyed by `"Migration Patterns"` IS found in the extracted conventions dictionary, and the generated task's Implementation Notes include the expected reference: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
5. **Bonus assertion:** Verify that no warning/error suppression is happening -- after the fix, the convention should be matched cleanly without fallback logic.

## Jira Comment (would be posted to ACME-500)

The following root cause analysis would be posted as an ADF comment on ACME-500:

**Root Cause:** The convention heading parser in plan-feature extracts section names via `line[3:]` without stripping trailing whitespace. Headings with trailing spaces produce mismatched dictionary keys, causing silent convention omission during task enrichment.

**Affected Files:**
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention heading extraction (`section_name = line[3:]`)
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment (`convention_name in discovered_conventions`)

**Suggested Approach:** Add `.strip()` to the heading extraction line (`section_name = line[3:].strip()`) to normalize whitespace. Optionally, add a warning log when a convention name is looked up but not found, to make future mismatches visible.

**Reproducer Strategy:** Create a CONVENTIONS.md fixture with trailing whitespace on a heading, run convention extraction, and assert that the convention is correctly matched and included in the generated task output.
