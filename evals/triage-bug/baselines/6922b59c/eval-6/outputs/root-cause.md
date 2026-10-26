# Step 4 -- Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention conformance analysis extracts `CONVENTIONS.md` section
headings using `line[3:]`, which captures all characters after the `## ` prefix without
stripping trailing whitespace. When a heading line contains trailing spaces (e.g.,
`## Migration Patterns  `), the extracted section name becomes `"Migration Patterns  "`
(with trailing spaces). The downstream convention-aware task enrichment performs an
exact-match lookup against the expected clean name `"Migration Patterns"`, which fails
because the dictionary key includes the trailing whitespace. The convention is silently
dropped from the generated task description with no warning or error.

## What Is Broken

The heading extraction logic in the convention conformance analysis does not normalize
whitespace. The line `section_name = line[3:]` preserves any trailing spaces, tabs, or
other whitespace characters present on the heading line in `CONVENTIONS.md`.

## Why It Is Broken

The code assumes that `CONVENTIONS.md` headings contain no trailing whitespace. This is
a fragile assumption because:

1. Many text editors add trailing whitespace silently
2. Copy-paste operations frequently introduce trailing whitespace
3. Markdown rendering is unaffected by trailing whitespace on headings, so authors have
   no visual feedback that whitespace is present
4. No validation or normalization step exists between extraction and lookup

## Where It Is Broken

- **Primary defect**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention
  heading extraction (`section_name = line[3:]`)
- **Secondary impact**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention
  lookup (`convention_name in discovered_conventions`) fails silently on mismatch

## How to Verify the Fix

A reproducer test should:

1. **Setup**: Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading
   (e.g., `## Migration Patterns  ` with two trailing spaces)
2. **Exercise**: Run the convention extraction logic against the fixture
3. **Assert (before fix)**: The convention is NOT found in the discovered conventions
   dictionary when looked up by the clean name `"Migration Patterns"` -- confirming the
   bug exists
4. **Assert (after fix)**: The convention IS found when looked up by the clean name
   `"Migration Patterns"` -- confirming the fix works
5. **Additional assertion**: Verify that no warning is suppressed -- if the fix includes
   adding a warning for unmatched conventions, test that no warning is emitted when
   whitespace is properly stripped

## Suggested Approach

Apply `.strip()` (or equivalent whitespace trimming) to the extracted section name:

```python
section_name = line[3:].strip()
```

This normalizes the heading text regardless of trailing whitespace, ensuring consistent
dictionary keys that match the expected clean convention names.

## Jira Comment (would be posted to ACME-500)

The following root cause analysis would be posted as an ADF comment on ACME-500:

**Root Cause**: The convention heading parser in plan-feature extracts section names using
`line[3:]` without stripping trailing whitespace. Headings with trailing spaces produce
dictionary keys that fail exact-match lookups, silently dropping the convention from
generated task descriptions.

**Affected Files**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- heading extraction and convention lookup

**Suggested Approach**: Add `.strip()` to the heading extraction (`section_name = line[3:].strip()`)
to normalize whitespace before storing in the conventions dictionary.

**Reproducer Strategy**: Create a CONVENTIONS.md fixture with trailing whitespace on headings
and verify that the convention is correctly matched and included in the generated task's
Implementation Notes.
