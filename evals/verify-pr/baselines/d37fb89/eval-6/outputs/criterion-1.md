# Criterion 1: Check 6 scans the PR diff for new public symbol definitions

## Verdict: PASS

## Reasoning

The PR diff adds section "6a -- Identify New Symbols" to `style-conventions.md` which instructs scanning the PR diff for "newly added function, method, struct, class, interface, enum, and type definitions." The check defines "new" as a symbol whose definition line appears in the diff with a `+` prefix and has no corresponding `-` line (not a rename or modification).

This directly satisfies the criterion: Check 6 scans the PR diff for new public symbol definitions.

## Evidence

From the diff in `style-conventions.md`:
```
+#### 6a — Identify New Symbols
+
+Scan the PR diff for newly added function, method, struct, class, interface,
+enum, and type definitions. A symbol is "new" if its definition line appears
+in the diff with a `+` prefix and has no corresponding `-` line (not a rename
+or modification of an existing symbol).
```
