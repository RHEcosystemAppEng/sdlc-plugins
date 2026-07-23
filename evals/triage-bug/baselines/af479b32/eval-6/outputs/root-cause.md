# Step 4 -- Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention conformance analysis extracts `CONVENTIONS.md` section headings using `line[3:]`, which preserves any trailing whitespace present on the heading line. When the extracted heading is used as a dictionary key, subsequent lookups by canonical convention name (without trailing whitespace) fail due to exact string mismatch. The convention is silently dropped with no warning or error logged.

## What Is Broken

The heading extraction logic in the plan-feature skill's convention conformance analysis does not normalize whitespace. The line `section_name = line[3:]` captures everything after the `## ` prefix, including trailing spaces and other whitespace characters. This raw string is used as the dictionary key in `conventions[section_name]`.

When the task enrichment step later attempts to match conventions using `if convention_name in discovered_conventions`, the canonical name (e.g., `"Migration Patterns"`) does not match the stored key (e.g., `"Migration Patterns  "`), so the convention is skipped entirely.

## Why It Is Broken

The code assumes that `CONVENTIONS.md` headings are free of trailing whitespace. This assumption is fragile because:

1. Many text editors silently add or preserve trailing whitespace.
2. Copy-paste operations can introduce trailing spaces.
3. Markdown renderers ignore trailing whitespace, so the document appears correct to users.
4. There is no validation or normalization step between extraction and lookup.

Additionally, the code has no fallback or warning mechanism -- when a convention is expected but not found in the dictionary, it is silently skipped rather than logged as a potential issue.

## Where It Is Broken

- **Primary defect**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention conformance analysis section, heading extraction line `section_name = line[3:]`
- **Secondary impact**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment section, exact-match lookup `convention_name in discovered_conventions`

## How to Verify the Fix

A reproducer test should:

1. **Setup**: Create a `CONVENTIONS.md` fixture with trailing whitespace on at least one heading (e.g., `## Migration Patterns  ` with two trailing spaces).
2. **Exercise**: Run the convention conformance analysis against the fixture with a feature that matches the whitespace-affected convention.
3. **Assert (before fix -- fails)**: The convention IS present in the extracted dictionary keys when looked up by canonical name (without trailing whitespace). This assertion will fail before the fix because the key contains trailing spaces.
4. **Assert (after fix -- passes)**: The convention IS present in the extracted dictionary keys. The generated task's Implementation Notes include the expected reference: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Suggested Approach

1. Add `.strip()` to the heading extraction: `section_name = line[3:].strip()`
2. Consider adding a warning log when a convention heading has trailing whitespace, to alert users to clean up their `CONVENTIONS.md` files.
3. Add a test fixture with trailing whitespace on headings to the plan-feature eval suite.

## Jira Comment (would be posted to ACME-500)

The following root cause analysis comment would be posted to the Bug issue:

**Root Cause**: The convention heading extraction in plan-feature uses `line[3:]` without stripping trailing whitespace. When `CONVENTIONS.md` headings have trailing spaces, the extracted section name includes those spaces, causing exact-match lookups to fail silently.

**Affected Files**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- heading extraction (`section_name = line[3:]`)
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention match lookup (`convention_name in discovered_conventions`)

**Suggested Approach**: Add `.strip()` to normalize heading text during extraction. Optionally add a warning when trailing whitespace is detected.

**Reproducer Strategy**: Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading, run convention conformance analysis, and assert the convention is correctly matched and included in the generated task output.
