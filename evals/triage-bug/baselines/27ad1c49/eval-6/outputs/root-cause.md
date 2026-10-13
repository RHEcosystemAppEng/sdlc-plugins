# Step 4 -- Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's CONVENTIONS.md parser extracts section headings using `line[3:]` (a simple substring slice after the `## ` prefix) without stripping trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted dictionary key retains those spaces (`"Migration Patterns  "`). The subsequent convention lookup uses the clean name (`"Migration Patterns"`) for an exact-match comparison via the `in` operator, which fails because the keys do not match. The convention is silently skipped with no warning or error logged.

## What Is Broken

The heading extraction in the convention conformance analysis produces whitespace-polluted dictionary keys. The `line[3:]` slice captures everything after `## `, including any trailing spaces or tabs before the newline.

## Why It Is Broken

The code assumes CONVENTIONS.md headings have no trailing whitespace. This is a fragile assumption because:
- Text editors commonly add or preserve trailing whitespace
- Copy-paste from other documents may introduce invisible trailing characters
- No input sanitization or normalization is applied to the extracted heading text
- No warning is emitted when a convention fails to match, making the failure completely silent

## Where It Is Broken

- **Primary defect**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention conformance analysis section, specifically the heading extraction line: `section_name = line[3:]`
- **Secondary impact**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment section, where the exact-match lookup `convention_name in discovered_conventions` silently fails

## How to Verify the Fix

A reproducer test should:

1. **Setup**: Create a CONVENTIONS.md fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces)
2. **Exercise**: Run the convention extraction logic against this fixture
3. **Assert (before fix)**: The convention with the trailing-whitespace heading is NOT found in the extracted conventions dictionary when looked up by the clean name -- confirming the bug
4. **Assert (after fix)**: The convention IS found when looked up by the clean name, proving the fix normalizes the heading text

The fix itself should apply `.strip()` (or `.rstrip()`) to the heading text after extraction:
```python
section_name = line[3:].strip()
```

## Suggested Approach

1. Add `.strip()` to the heading extraction: `section_name = line[3:].strip()`
2. This normalizes all heading keys, making the lookup robust against trailing whitespace
3. Consider also stripping on the lookup side for defense-in-depth, though fixing extraction is the primary fix

## Reproducer Strategy

- Create a new eval fixture file (e.g., `evals/plan-feature/files/conventions-trailing-whitespace.md`) with headings that include trailing spaces
- Write an eval test case that runs plan-feature convention extraction against this fixture
- Assert that the convention is correctly matched and included in the generated task's Implementation Notes
- This covers the specific edge case currently missing from `evals/plan-feature/files/conventions-mock.md`

## Jira Comment (would be posted to ACME-500)

The following root cause analysis comment would be posted to the bug issue:

**Root Cause**: The plan-feature skill extracts CONVENTIONS.md headings with `line[3:]`, which preserves trailing whitespace. The downstream convention lookup uses exact string matching, so headings with trailing spaces are silently skipped. No warning is logged.

**Affected Files**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- heading extraction (`line[3:]`) and convention lookup (`convention_name in discovered_conventions`)

**Suggested Approach**: Apply `.strip()` to the extracted heading text to normalize whitespace before storing as a dictionary key.

**Reproducer Strategy**: Create a CONVENTIONS.md fixture with trailing whitespace on a heading, run the convention extraction, and assert the convention is found by its clean name.
