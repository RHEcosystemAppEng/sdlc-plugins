# Root Cause Analysis -- Step 4

## Root Cause

The plan-feature skill's convention heading extraction uses `line[3:]` to extract the section name from `## `-prefixed lines in `CONVENTIONS.md`. This slicing operation preserves any trailing whitespace present on the heading line. When a heading is written as `## Migration Patterns  ` (with trailing spaces), the extracted key becomes `"Migration Patterns  "` instead of `"Migration Patterns"`.

The downstream convention-matching logic uses exact string comparison (`convention_name in discovered_conventions`) to look up conventions by name. Since the expected convention name `"Migration Patterns"` does not match the stored key `"Migration Patterns  "`, the lookup silently fails and the convention is dropped from the generated task description. No warning or error is emitted.

## What Is Broken

The heading extraction logic does not normalize trailing whitespace when parsing `CONVENTIONS.md` section headings. The extracted section name retains trailing spaces, causing exact-match lookups to fail silently.

## Why It Is Broken

The `line[3:]` slice extracts everything after `## ` without calling `.strip()` or `.rstrip()` on the result. This is a missing input-normalization step. The author likely assumed heading lines would not contain trailing whitespace, but Markdown editors and manual editing commonly introduce trailing spaces.

## Where It Is Broken

- **Primary defect**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention heading extraction logic (`section_name = line[3:]`)
- **Secondary impact**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment (`convention_name in discovered_conventions`)

## How to Verify the Fix

A reproducer test should:

1. **Setup**: Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces)
2. **Execute**: Run the convention extraction logic against the fixture
3. **Assert (before fix)**: The convention is NOT found when looked up by its clean name `"Migration Patterns"` -- confirming the bug
4. **Assert (after fix)**: The convention IS found when looked up by its clean name `"Migration Patterns"` -- confirming the fix works
5. **Assert**: The generated task's Implementation Notes include the expected convention reference: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

## Suggested Approach

Apply `.strip()` (or `.rstrip()`) to the extracted section name in the heading extraction logic:

```python
section_name = line[3:].strip()
```

This normalizes the key regardless of trailing whitespace in the source file. No changes are needed to the downstream matching logic, since the stored keys will now be clean.

## Reproducer Strategy

- Add a new eval fixture file (e.g., `evals/plan-feature/files/conventions-trailing-ws-mock.md`) with trailing whitespace on headings
- Write a test case that feeds this fixture through the convention extraction and asserts that the convention is found by its clean name
- Verify that the generated task description includes the expected convention reference
