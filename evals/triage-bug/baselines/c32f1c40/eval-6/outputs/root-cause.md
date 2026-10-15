# Step 4 -- Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention conformance analysis extracts `CONVENTIONS.md`
section headings using `line[3:]` (slicing off the `## ` prefix) without stripping
trailing whitespace. When a heading line contains trailing spaces (e.g.,
`## Migration Patterns  `), the extracted section name becomes `"Migration Patterns  "`
instead of `"Migration Patterns"`. The subsequent convention lookup uses exact string
matching (`convention_name in discovered_conventions`), which fails silently because
the whitespace-padded key does not match the clean expected key. No warning or error
is emitted, causing the convention to be silently dropped from the generated task's
Implementation Notes.

## What Is Broken

The heading extraction logic in the plan-feature skill's convention conformance
analysis does not normalize whitespace. The string slice `line[3:]` preserves any
trailing whitespace present in the source file, creating dictionary keys that cannot
be matched by the enrichment step.

## Why It Is Broken

The code assumes that `CONVENTIONS.md` headings have no trailing whitespace. This is
a fragile assumption -- many text editors add trailing whitespace, and Markdown
renderers ignore it, so users have no visual indication of the problem. The lack of
`.strip()` on the extracted heading text creates a silent data mismatch.

## Where It Is Broken

- **Primary defect**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` --
  convention heading extraction logic, specifically `section_name = line[3:]`
  (missing `.strip()` call).
- **Secondary location**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` --
  convention-aware task enrichment, where the exact match lookup propagates the
  failure silently without logging a warning.

## How to Verify the Fix

A reproducer test should:

1. **Setup**: Create a `CONVENTIONS.md` fixture with trailing whitespace on at least
   one heading line (e.g., `## Migration Patterns  ` with two trailing spaces).
2. **Trigger**: Run the plan-feature convention conformance analysis against a
   feature that should match the whitespace-padded convention.
3. **Assert (before fix)**: The generated task's Implementation Notes do NOT contain
   the expected convention reference -- confirming the bug.
4. **Assert (after fix)**: The generated task's Implementation Notes DO contain
   `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.`
   -- confirming the fix works.

## Suggested Approach

1. Add `.strip()` to the heading extraction: `section_name = line[3:].strip()`
2. Optionally add a warning log when a convention heading is found with trailing
   whitespace, to aid debugging.
3. Consider also stripping the lookup key in the enrichment step for defense in depth.

## Jira Comment (would be posted to ACME-500)

The root cause comment would be posted via `jira.add_comment("ACME-500", ...)` in
ADF format, containing:

- **Root Cause**: Convention heading extraction uses `line[3:]` without `.strip()`,
  causing trailing whitespace in section names to break exact-match lookups.
- **Affected Files**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
  (heading extraction and convention-aware enrichment sections).
- **Suggested Approach**: Add `.strip()` to heading extraction; optionally add
  warning log for whitespace-padded headings.
- **Reproducer Strategy**: Create a CONVENTIONS.md fixture with trailing whitespace
  on a heading, run plan-feature, and assert the convention appears in the generated
  task's Implementation Notes.

Comment would include the Comment Footnote with plugin version and link to
https://github.com/RHEcosystemAppEng/sdlc-plugins.
