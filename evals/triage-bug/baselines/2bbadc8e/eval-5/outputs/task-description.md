## Repository
acme-backend

## Target Branch
main

## Description
Fix the dark mode preference persistence failure caused by trailing whitespace in heading extraction logic. The heading parser uses `line[3:]` without stripping trailing whitespace, producing keys like `"Dark Mode  "` that fail exact-match lookups against expected preference identifiers. This causes the dark mode toggle to silently fail to persist, reverting to light mode on the next browser session. Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction at `line[3:]` to remove trailing whitespace from parsed section names

## Implementation Notes
The root cause is in the heading extraction loop within `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The fix is to change `line[3:]` to `line[3:].strip()` so that trailing spaces on heading lines (e.g., `## Dark Mode  \n`) are removed before the key is stored.

The downstream exact-match comparison in the convention-aware task enrichment step:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This match currently fails when the extracted key has trailing whitespace. After the fix, keys will be normalized and the lookup will succeed.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings, so this edge case is not covered by current tests. The reproducer test must create a fixture with trailing whitespace to expose the bug.

No `CONVENTIONS.md` exists at the repository root, so no repository-specific conventions apply.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a mock conventions/settings content with trailing whitespace on headings (e.g., `## Dark Mode  `), runs the extraction logic, and asserts the key matches `"Dark Mode"` without trailing whitespace. The test must fail before the fix and pass after.
- [ ] The heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` strips trailing whitespace from extracted section names using `.strip()`
- [ ] The convention-aware task enrichment exact-match lookup succeeds for headings with trailing whitespace
- [ ] No regression in existing tests (`evals/plan-feature/` test suite passes)

## Test Requirements
- [ ] Reproducer test: create a fixture with heading `## Dark Mode  ` (trailing spaces). Parse it through the heading extraction logic. Assert the extracted key is `"Dark Mode"` (no trailing whitespace). Assert the preference/convention lookup succeeds for this key. This test must fail before the fix and pass after.
- [ ] Edge case test: verify headings with no trailing whitespace continue to work correctly (regression guard)
- [ ] Edge case test: verify headings with mixed whitespace types (tabs, multiple spaces) are handled by `.strip()`

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open application, navigate to Settings > Appearance, toggle Dark Mode to ON, close browser completely, reopen browser and navigate back to the application
- **Expected Result**: The application should load in dark mode, matching the user's last preference
- **Actual Result**: The application loads in light mode; the dark mode toggle is reset to OFF
- **Root Cause**: Heading extraction uses `line[3:]` without `.strip()`, producing keys with trailing whitespace that fail exact-match lookups. The dark mode preference is never persisted because the key match fails silently.
