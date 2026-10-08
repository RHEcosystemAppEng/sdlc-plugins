## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing whitespace in convention heading extraction that causes convention-aware task enrichment lookups to fail silently. The heading parser at `line[3:]` does not strip trailing whitespace, so section names like `"Migration Patterns  "` fail exact-match comparison against expected names like `"Migration Patterns"`. This causes convention guidance to be silently dropped from generated tasks. Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to convention heading extraction to normalize section names

## Implementation Notes
The convention heading extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` parses CONVENTIONS.md headings using:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]
        conventions[section_name] = current_section_content
```

The fix is to change `line[3:]` to `line[3:].strip()` so that trailing whitespace on heading lines is removed before storing the section name in the dictionary.

The downstream convention-aware task enrichment performs exact-match lookup:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

After the fix, this lookup will succeed regardless of trailing whitespace in the CONVENTIONS.md source file.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not cover this edge case -- the reproducer test must use a fixture with trailing whitespace on headings.

The repository does not have a CONVENTIONS.md at its root.

## Acceptance Criteria
- [ ] Reproducer test: a test that parses a CONVENTIONS.md fixture with trailing whitespace on headings and asserts that convention-aware enrichment lookups succeed (fails before fix, passes after)
- [ ] Convention heading extraction strips trailing whitespace from parsed section names using `.strip()`
- [ ] Convention-aware task enrichment matches sections correctly when CONVENTIONS.md headings contain trailing whitespace
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with at least one heading containing trailing spaces (e.g., `## Migration Patterns  `). Parse it through the convention extraction logic. Assert: (1) the extracted section name equals `"Migration Patterns"` (no trailing spaces), (2) a subsequent lookup for `"Migration Patterns"` in the conventions dictionary succeeds, (3) the enrichment note is appended to the task output
- [ ] Verify that headings without trailing whitespace continue to parse correctly (no regression)
- [ ] Verify that headings with mixed whitespace (tabs, multiple spaces) are also handled

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: 1. Open the application. 2. Navigate to Settings > Appearance. 3. Toggle "Dark Mode" to ON. 4. Close the browser completely. 5. Reopen the browser and navigate back to the application.
- **Expected Result**: The application should load in dark mode, matching the user's last preference.
- **Actual Result**: The application loads in light mode. The dark mode toggle is reset to OFF.
- **Root Cause**: Convention heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` uses `line[3:]` without `.strip()`, causing trailing whitespace in CONVENTIONS.md headings to break exact-match lookups in convention-aware task enrichment, silently dropping persistence-related convention guidance.
