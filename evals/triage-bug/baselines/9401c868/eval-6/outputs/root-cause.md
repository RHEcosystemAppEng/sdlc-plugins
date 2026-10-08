# Step 4 -- Root Cause Analysis: ACME-500

## Root Cause

The plan-feature skill's convention conformance analysis extracts CONVENTIONS.md section headings using `line[3:]`, which captures the raw text after the `## ` prefix without stripping trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted section name becomes `"Migration Patterns  "` instead of `"Migration Patterns"`. The subsequent dictionary lookup in the task enrichment step uses exact string comparison (`convention_name in discovered_conventions`), which fails to match the whitespace-padded key against the expected clean key. The convention is silently dropped from the generated task description with no warning or error.

## What Is Broken

The heading text extraction in the convention lookup code does not normalize whitespace. The expression `line[3:]` preserves any trailing spaces present in the source file. Since CONVENTIONS.md files are human-authored, trailing whitespace is a common and expected occurrence that the parser must tolerate.

## Why It Is Broken

The code assumes CONVENTIONS.md headings have no trailing whitespace. There is no `.strip()` or `.rstrip()` call on the extracted heading text, and no fuzzy matching or whitespace-tolerant comparison is used during the convention lookup step.

## Where It Is Broken

| File | Symbol/Location | Role |
|------|----------------|------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Extracts heading without stripping whitespace |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact-match lookup fails on whitespace-padded keys |

## How to Verify the Fix

A reproducer test should:

1. **Set up** a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces).
2. **Run** the convention extraction logic against this fixture.
3. **Assert** that the extracted section name is `"Migration Patterns"` (trimmed), not `"Migration Patterns  "` (with trailing spaces).
4. **Assert** that the convention-aware task enrichment successfully matches and includes the convention in the generated task's Implementation Notes, producing output like: `Per CONVENTIONS.md "Migration Patterns": add Index::create() for all FK columns.`

## Reproducer Strategy

- Create an eval fixture (`evals/plan-feature/files/conventions-trailing-ws-mock.md`) with headings that include trailing whitespace.
- Write a test that invokes the convention extraction and enrichment pipeline against this fixture.
- Verify that the generated task description includes the convention reference that is currently being dropped.
- The test should fail before the fix (convention silently dropped) and pass after the fix (convention correctly included).

## Jira Comment (would be posted to ACME-500)

The following root cause analysis would be posted as an ADF comment on ACME-500:

**Root Cause**: The convention heading extraction in plan-feature uses `line[3:]` without stripping trailing whitespace. When CONVENTIONS.md headings have trailing spaces, the extracted section name includes them, causing the exact-match dictionary lookup to fail silently. The convention is dropped from the generated task description with no warning.

**Affected Files**:
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention heading extraction (`line[3:]`)
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- convention-aware task enrichment (exact-match lookup)

**Suggested Approach**: Add `.strip()` to the heading extraction (`section_name = line[3:].strip()`) so that trailing whitespace is normalized before dictionary storage. Optionally, add a warning log when a convention match fails to aid future debugging.

**Reproducer Strategy**: Create an eval fixture with trailing whitespace on convention headings and verify that the plan-feature skill correctly includes the convention in the generated task's Implementation Notes.
