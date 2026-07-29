## Repository
acme-backend

## Target Branch
main

## Description
Fix convention heading extraction in the plan-feature skill to strip trailing whitespace from parsed CONVENTIONS.md headings. Currently, `line[3:]` retains trailing spaces, causing exact-match lookups in the convention-aware task enrichment step to silently fail. Fixes ACME-511.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- apply `.strip()` to the heading extraction at `line[3:]` so that trailing whitespace is removed from convention section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with CONVENTIONS.md headings that include trailing whitespace to cover this edge case

## Implementation Notes
The defect is in the convention heading extraction logic within the plan-feature skill. The relevant code path:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The fix is to apply `.strip()` to normalize the extracted heading:

```python
section_name = line[3:].strip()
```

The downstream consumer that fails is the convention-aware task enrichment:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

This exact-match lookup silently fails when dictionary keys contain trailing whitespace. After the fix, all keys will be normalized and lookups will succeed regardless of source file formatting.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. Create a new fixture that includes headings like `## Migration Patterns  ` (with trailing spaces) to cover this edge case.

No CONVENTIONS.md exists at the repository root. No repository-level conventions apply to this fix.

## Acceptance Criteria
- [ ] Reproducer test: a test using a CONVENTIONS.md fixture with trailing-whitespace headings demonstrates that convention matching fails before the fix and succeeds after the fix
- [ ] Convention heading extraction applies `.strip()` to `line[3:]` so trailing whitespace is removed
- [ ] Convention-aware task enrichment correctly matches and includes conventions from headings with trailing whitespace
- [ ] No regression in existing plan-feature evals and tests

## Test Requirements
- [ ] Reproducer test: create a mock CONVENTIONS.md with headings containing trailing whitespace (e.g., `## Migration Patterns  `), run the convention extraction logic, and assert that (a) the extracted section names do not contain trailing whitespace and (b) the task enrichment step successfully matches and applies the convention content
- [ ] Verify that the existing eval fixture (`evals/plan-feature/files/conventions-mock.md`) without trailing whitespace continues to work correctly after the fix

## Bug Context

- **Bug**: [ACME-511](https://mock-jira.example.com/browse/ACME-511)
- **Steps to Reproduce**: Open the application, navigate to Settings > Appearance, toggle Dark Mode to ON, close the browser completely, reopen the browser and navigate back to the application
- **Expected Result**: The application should load in dark mode, matching the user's last preference
- **Actual Result**: The application loads in light mode; the dark mode toggle is reset to OFF
- **Root Cause**: Convention heading extraction in the plan-feature skill uses `line[3:]` without stripping trailing whitespace, causing exact-match convention lookups to silently fail when CONVENTIONS.md headings contain trailing spaces
