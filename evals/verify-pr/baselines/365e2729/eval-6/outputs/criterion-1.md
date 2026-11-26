# Criterion 1 — Check 6 scans the PR diff for new public symbol definitions

**Verdict: FAIL (partially met)**

## What the criterion requires
Check 6 must scan the PR diff and find new **public** symbol definitions. The task Description also says "new public symbols".

## What the PR implements
`style-conventions.md`, new section `#### 6a — Identify New Symbols`:

> Scan the PR diff for newly added function, method, struct, class, interface, enum, and type definitions. A symbol is "new" if its definition line appears in the diff with a `+` prefix and has no corresponding `-` line (not a rename or modification of an existing symbol).

## Reasoning
- **Met:** the scanning part. 6a scans the PR diff (`+` lines with no matching `-` line) for definitions of every relevant symbol kind (function, method, struct, class, interface, enum, type). That is broader than the task's Implementation Notes ask for.
- **Not met:** the "public" qualifier. The intro paragraph of Check 6 says "new public symbols", but 6a, 6b and 6c never put that into practice:
  - There is no rule for telling public symbols from private ones. Examples of what is missing: Rust `pub`, Java/TS `public`/`export`, Go identifiers that start with a capital letter, Python names without a leading `_`.
  - As written, every new definition is counted, including private helpers, private methods and non-exported functions.
- **Effect:** Documentation Coverage would raise false WARNs on private symbols, which goes against the criterion's intent.
- **Contributing cause:** the task's Implementation Notes say "new function/method/struct/class definitions" and leave out "public". The criterion itself is clear, though, and verification follows the Acceptance Criteria.

## Evidence
- PR diff, `style-conventions.md` hunk `@@ -282,6 +282,48 @@`: Check 6 intro (says "public") and 6a (no visibility filter).

## Follow-up
Sub-task 3 (restrict Check 6a to public/exported symbols).
