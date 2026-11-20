# Criterion 1: Check 6 scans the PR diff for new public symbol definitions

**Verdict: PASS**

## Evidence
`plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, new sub-step **6a — Identify New Symbols**:

> Scan the PR diff for newly added function, method, struct, class, interface,
> enum, and type definitions. A symbol is "new" if its definition line appears
> in the diff with a `+` prefix and has no corresponding `-` line (not a rename
> or modification of an existing symbol).

The Check 6 intro limits the scope to "new public symbols introduced in the PR".

## Reasoning
- Check 6 scans the **PR diff**. It does not scan the whole codebase.
- "New" has a working definition: a `+` definition line with no matching `-` line. That definition leaves out renames and modified symbols.
- The symbol kinds cover function, method, struct, class, interface, enum and type. That is a superset of the Implementation Notes list ("function/method/struct/class").

## Observation (non-blocking)
Step 6a has no explicit visibility filter. It does not mention `pub`, `export`, capitalized Go identifiers or a `_` prefix in Python. Only the intro paragraph says "public", so private helpers could also be flagged. The Implementation Notes do not ask for a visibility filter either, so the criterion is still met. A clarifying sentence in 6a would make the check more precise.
