# Criterion 1: `PackageSummary` includes a `vulnerability_count: i64` field

**Verdict: PASS**

## What was checked
- `modules/fundamental/src/package/model/summary.rs` in the PR diff.

## What was found
The diff adds the following to the `PackageSummary` struct:

```rust
/// Number of known vulnerability advisories affecting this package.
pub vulnerability_count: i64,
```

The field has the name and type the criterion asks for (`i64`). It is `pub`, has a doc comment, and sits after the existing `license` field, which matches the existing field pattern described in the Implementation Notes.
