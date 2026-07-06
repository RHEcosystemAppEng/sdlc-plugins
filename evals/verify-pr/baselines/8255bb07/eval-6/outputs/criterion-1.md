## Criterion 1: Check 6 scans the PR diff for new public symbol definitions

### Verdict: PASS

### Reasoning

The PR diff adds a new "Check 6 -- Documentation Coverage" section to
`plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. Within this
section, step **6a -- Identify New Symbols** explicitly instructs the sub-agent
to:

> Scan the PR diff for newly added function, method, struct, class, interface,
> enum, and type definitions. A symbol is "new" if its definition line appears
> in the diff with a `+` prefix and has no corresponding `-` line (not a rename
> or modification of an existing symbol).

This directly satisfies the criterion. The check scans the PR diff for new
public symbol definitions, covering the full range of symbol types (function,
method, struct, class, interface, enum, type). The definition of "new" is
precise -- it requires a `+` prefix line with no corresponding `-` line,
correctly excluding renames and modifications.

### Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines: the new step 6a section (lines 17-23 of the added block)
- The check covers functions, methods, structs, classes, interfaces, enums,
  and type definitions
