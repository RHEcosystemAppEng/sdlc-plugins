# Criterion 1: Check 6 scans the PR diff for new public symbol definitions

**Verdict: PASS**

## Evidence

`plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` adds `### Check 6 — Documentation Coverage` with sub-step `#### 6a — Identify New Symbols`:

> Scan the PR diff for newly added function, method, struct, class, interface, enum, and type definitions. A symbol is "new" if its definition line appears in the diff with a `+` prefix and has no corresponding `-` line (not a rename or modification of an existing symbol).

The check intro states its purpose is to verify "that new public symbols introduced in the PR have documentation comments".

## Reasoning

- The check explicitly targets the PR diff as its input (`+`-prefixed definition lines).
- It covers the symbol kinds from the task's Implementation Notes (function/method/struct/class) and goes further (interface, enum, type).
- It defines "new" clearly: added lines with no matching removed line, so renames and edits are excluded.

## Advisory (does not change the verdict)

Sub-step 6a never filters by visibility. It does not mention `pub` (Rust), `export` (TypeScript), `public` (Java), capitalized identifiers (Go), or the leading-underscore convention (Python). The "public" restriction appears only in the check's intro sentence. As written, Check 6 may also flag private or internal helpers. That is stricter than the criterion asks, not a gap in coverage, but a short visibility rule in 6a would make the intent explicit.
