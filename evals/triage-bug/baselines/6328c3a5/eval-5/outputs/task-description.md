## Repository
acme-backend

## Target Branch
main

## Description
Fix the convention heading extraction in the plan-feature skill to strip trailing
whitespace from parsed section names. The current code (`line[3:]`) preserves
trailing spaces from the source file, causing exact-match lookups against
convention names to fail silently. This results in user preferences and convention
rules being ignored when the source configuration contains trailing whitespace on
heading lines. Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction at `line[3:]` to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on convention headings for reproducer test

## Implementation Notes
The bug is in the convention heading extraction loop in
`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The relevant code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

**Fix**: Change `line[3:]` to `line[3:].strip()` so that extracted section names
are normalized regardless of trailing whitespace in the source file.

The downstream lookup that fails is:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match fails when `convention_name` (e.g., `"Migration Patterns"`) is compared
against a key with trailing spaces (e.g., `"Migration Patterns  "`). After the fix,
the dictionary keys will be stripped, restoring correct lookups.

**Reproducer test guidance**:
- Create a conventions mock file with headings that have trailing whitespace
  (e.g., `## Migration Patterns  ` with 2+ trailing spaces)
- Run the heading extraction logic against this fixture
- The test should FAIL before the fix (extracted name includes trailing spaces)
  and PASS after (extracted name is stripped)

**Existing test patterns**: See `evals/plan-feature/files/conventions-mock.md` for
the existing conventions fixture format. The new fixture should follow the same
structure but include trailing whitespace on headings.

The repository does not have a root `CONVENTIONS.md` file.

## Acceptance Criteria
- [ ] Reproducer test: a test with a conventions file containing trailing whitespace on headings demonstrates that heading extraction produces clean names (fails before fix, passes after)
- [ ] The heading extraction code in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` strips trailing whitespace from extracted section names using `.strip()`
- [ ] Convention-aware task enrichment successfully matches conventions when source headings have trailing whitespace
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a conventions mock file with trailing whitespace on at least one `## ` heading (e.g., `## Migration Patterns  `). Parse it through the heading extraction logic and assert that the resulting dictionary key equals `"Migration Patterns"` (no trailing spaces). Assert that the convention-aware enrichment step finds the convention by its canonical name.
- [ ] Verify that the existing conventions mock (without trailing whitespace) continues to work correctly after the fix -- no regressions in normal-case heading extraction.

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open app, navigate to Settings > Appearance, toggle Dark Mode to ON, close browser, reopen browser and navigate back to app.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Convention/settings heading extraction (`line[3:]`) does not strip trailing whitespace, causing exact-match preference lookups to fail silently when source headings contain trailing spaces. The preference value is stored but its key is not found on subsequent reads.
