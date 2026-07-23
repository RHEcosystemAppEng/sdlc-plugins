## Repository
acme-backend

## Target Branch
main

## Description
Fix convention heading extraction to strip trailing whitespace, which prevents convention-driven settings (including user preference persistence such as dark mode) from being applied. The extraction logic uses `line[3:]` without calling `.strip()`, causing exact-match lookups to fail when `CONVENTIONS.md` headings contain trailing spaces. Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to convention heading extraction (`section_name = line[3:]`)

## Files to Create
- `evals/plan-feature/files/conventions-whitespace-mock.md` -- test fixture with trailing whitespace on headings for reproducer test

## Implementation Notes
The defect is in the convention heading extraction logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]
```

must be changed to:

```python
section_name = line[3:].strip()
```

**Reproducer test guidance (from Steps to Reproduce):**

- **Input/scenario that triggers the bug**: A `CONVENTIONS.md` file with at least one heading that has trailing whitespace, e.g., `## Dark Mode Preferences  ` (two trailing spaces). The convention heading extraction is run against this file, followed by a convention-aware task enrichment lookup using the canonical name `"Dark Mode Preferences"`.
- **Incorrect behavior (Actual Result)**: The extracted section name is `"Dark Mode Preferences  "` (with trailing spaces). The exact-match lookup `convention_name in discovered_conventions` fails because the canonical name does not match. The dark mode preference setting is not applied; the application reverts to light mode on browser restart.
- **Correct behavior (Expected Result)**: The extracted section name is `"Dark Mode Preferences"` (trimmed). The exact-match lookup succeeds. The dark mode preference is persisted and applied across browser sessions.

**Existing test patterns**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` tests convention parsing but does NOT include trailing whitespace on headings. The new fixture should mirror its structure but add trailing whitespace to at least one heading to cover this edge case.

**Code paths involved**:
- Convention heading extraction: iterates over `CONVENTIONS.md` lines, matches `## ` prefix, extracts `line[3:]` as section name
- Convention-aware task enrichment: looks up `convention_name in discovered_conventions` dictionary for exact match

No `CONVENTIONS.md` exists at the repository root, so no additional project conventions apply to this fix.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing conventions fixture; use as structural reference for the new whitespace-variant fixture

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on headings demonstrates that convention heading extraction returns trimmed section names (fails before fix, passes after fix)
- [ ] Convention heading extraction applies `.strip()` to heading text after `line[3:]` extraction
- [ ] Convention-aware task enrichment correctly matches conventions when source headings have trailing whitespace
- [ ] No regression in existing plan-feature evals and convention parsing tests

## Test Requirements
- [ ] Reproducer test: create a conventions fixture with trailing whitespace on at least one heading (e.g., `## Dark Mode Preferences  `), run the heading extraction logic, and assert the extracted key equals the canonical name without trailing whitespace. Then run convention-aware task enrichment with the canonical name and assert the convention is found and its content is applied.
- [ ] Verify that the existing `evals/plan-feature/files/conventions-mock.md` fixture (without trailing whitespace) continues to pass without changes
- [ ] Edge case: heading with only whitespace after `## ` prefix should extract as empty string, not whitespace

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open app, navigate to Settings > Appearance, toggle Dark Mode ON, close browser completely, reopen browser and navigate back to the app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Convention heading extraction at `line[3:]` does not strip trailing whitespace, causing exact-match lookups in convention-aware task enrichment to fail silently. Convention-driven preference persistence (dark mode) is not applied.
