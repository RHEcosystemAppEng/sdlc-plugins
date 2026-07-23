# Step 4 -- Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention heading extraction uses `line[3:]` to extract the section name after the `## ` markdown prefix, but does not call `.strip()` on the result. When a `CONVENTIONS.md` heading line contains trailing whitespace (e.g., `## Migration Patterns  `), the extracted key becomes `"Migration Patterns  "` instead of `"Migration Patterns"`. The subsequent exact-match lookup (`convention_name in discovered_conventions`) fails silently because the key with trailing spaces does not match the expected clean key. No warning or error is logged, so the convention is silently dropped from the generated task description.

## What is Broken

The heading extraction logic in the plan-feature skill's convention conformance analysis does not normalize whitespace. The line `section_name = line[3:]` preserves any trailing spaces from the source file, creating dictionary keys that cannot be matched by downstream lookups.

## Why it is Broken

The code assumes that `CONVENTIONS.md` headings contain no trailing whitespace. This is a fragile assumption -- many text editors add trailing whitespace, and markdown renderers ignore it. The extraction should be whitespace-tolerant.

## Where it is Broken

- **Primary**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention conformance analysis section, heading extraction logic (`line[3:]` without `.strip()`)
- **Secondary**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment section, exact-match lookup (`convention_name in discovered_conventions`)

## How to Verify the Fix

A reproducer test should:

1. Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces).
2. Run the convention conformance analysis against a feature that matches that convention section.
3. Assert that the generated task's Implementation Notes include the convention reference (e.g., `Per CONVENTIONS.md Migration Patterns: ...`).
4. The test should fail before the fix (convention silently dropped) and pass after (convention correctly included).

## Suggested Approach

Add `.strip()` to the heading extraction line:

```python
section_name = line[3:].strip()
```

This normalizes the key regardless of trailing whitespace in the source file. No changes are needed to the downstream lookup logic since it already uses the correct (clean) key for comparison.

## Jira Comment (Step 4 Output)

The following root cause analysis would be posted as a comment on ACME-500:

**Root Cause**: The plan-feature skill extracts CONVENTIONS.md section headings using `line[3:]` without stripping trailing whitespace. When headings have trailing spaces, the extracted key mismatches the expected clean key during convention lookup, causing the convention to be silently dropped.

**Affected Files**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- heading extraction (`line[3:]` without `.strip()`)
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment (exact-match lookup)

**Suggested Approach**: Add `.strip()` to the heading extraction: `section_name = line[3:].strip()`. This normalizes whitespace without affecting the downstream lookup logic.

**Reproducer Strategy**: Create a CONVENTIONS.md fixture with trailing whitespace on headings. Run plan-feature against a feature matching that convention. Assert the convention appears in the generated task's Implementation Notes. Test should fail before fix and pass after.
