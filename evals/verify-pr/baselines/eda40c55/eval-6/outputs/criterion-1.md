## Criterion 1: Check 6 scans the PR diff for new public symbol definitions

### Verdict: PASS

### Analysis

The PR diff adds step "6a -- Identify New Symbols" to `style-conventions.md` which explicitly instructs the sub-agent to:

> Scan the PR diff for newly added function, method, struct, class, interface, enum, and type definitions.

The step further defines what constitutes a "new" symbol:

> A symbol is "new" if its definition line appears in the diff with a `+` prefix and has no corresponding `-` line (not a rename or modification of an existing symbol).

This covers the full range of public symbol types across languages and correctly scopes to additions only (ignoring renames and modifications). The implementation directly addresses the acceptance criterion by scanning the PR diff for new public symbol definitions.

### Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Lines added in diff: "6a -- Identify New Symbols" section (lines 17-23 in the diff hunk)
- Symbol types covered: function, method, struct, class, interface, enum, type
- Scoping rule: `+` prefix with no corresponding `-` line
