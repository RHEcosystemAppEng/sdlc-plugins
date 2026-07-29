# Step 4 -- Root Cause Analysis: ACME-511

## Root Cause

The convention heading extraction in the plan-feature skill uses `line[3:]` to
extract the heading text after the `## ` prefix, but does not strip trailing
whitespace from the result. When a `CONVENTIONS.md` file contains headings with
trailing spaces (e.g., `## Migration Patterns  `), the extracted section name
retains those spaces. Downstream, the convention-aware task enrichment performs
an exact-match lookup against the discovered conventions dictionary, which fails
because the key `"Migration Patterns  "` does not equal the expected
`"Migration Patterns"`.

This causes convention-derived implementation notes to be silently dropped from
generated tasks, even when the relevant convention section exists in the
repository's CONVENTIONS.md file.

## What Is Broken

The string extraction logic at `line[3:]` in the convention heading parser
produces keys with trailing whitespace that do not match expected convention
names used in downstream lookups.

## Why It Is Broken

The `line[3:]` slice captures everything after the `## ` prefix, including any
trailing spaces or whitespace characters present on the heading line. No `.strip()`
call is applied to normalize the extracted name. Since the downstream enrichment
step uses exact string matching (`convention_name in discovered_conventions`),
any trailing whitespace causes a silent lookup failure.

## Where It Is Broken

| File | Location |
|---|---|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction: `section_name = line[3:]` |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment: `if convention_name in discovered_conventions` |

## How to Verify the Fix

A reproducer test should:

1. Create a mock CONVENTIONS.md with headings that include trailing whitespace
   (e.g., `## Migration Patterns  ` with trailing spaces).
2. Run the convention heading extraction logic against this mock file.
3. Assert that the extracted section names are stripped of trailing whitespace.
4. Assert that the convention-aware task enrichment successfully matches and
   includes the convention content in the generated task's Implementation Notes.

The test should fail before the fix (trailing whitespace causes match failure)
and pass after the fix (`.strip()` normalizes the heading names).

## Suggested Approach

Apply `.strip()` to the extracted heading text: `section_name = line[3:].strip()`.
This normalizes all heading names regardless of trailing whitespace in the source
file, ensuring exact-match lookups succeed consistently.

## Reproducer Strategy

Add a new eval fixture (or modify the existing `evals/plan-feature/files/conventions-mock.md`)
to include headings with trailing whitespace. Write a test that exercises the
convention extraction and enrichment pipeline with this fixture, asserting that
conventions are correctly discovered and applied despite trailing whitespace.
