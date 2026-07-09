# Criterion 1: Check 6 scans the PR diff for new public symbol definitions

## Verdict: PASS

## Reasoning

The PR diff adds section "6a -- Identify New Symbols" to `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This section explicitly instructs the sub-agent to:

> Scan the PR diff for newly added function, method, struct, class, interface,
> enum, and type definitions. A symbol is "new" if its definition line appears
> in the diff with a `+` prefix and has no corresponding `-` line (not a rename
> or modification of an existing symbol).

This directly satisfies the criterion. The check identifies new public symbol definitions by scanning the PR diff for added definition lines across six symbol categories (function, method, struct, class, interface, enum, and type). The `+` prefix / no corresponding `-` line heuristic correctly distinguishes genuinely new symbols from renames or modifications.

## Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines: the `#### 6a -- Identify New Symbols` section (diff lines 17-23)
- Symbol types covered: function, method, struct, class, interface, enum, type
- Newness heuristic: `+` prefix with no corresponding `-` line
