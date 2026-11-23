# File 2 — MODIFY `modules/fundamental/src/advisory/model/mod.rs`

**Purpose**: register the new model module (as the task's Files to Modify requires).

**Inspect first**: `get_symbols_overview` to see the existing `pub mod summary; pub mod details;`
lines and whether siblings are re-exported (`pub use summary::*;`).

**Change** (additive, alphabetical with the existing declarations):

```rust
pub mod details;
pub mod severity_summary;   // NEW
pub mod summary;
```

If the file re-exports sibling types (e.g. `pub use summary::AdvisorySummary;`), add the matching
`pub use severity_summary::SeveritySummary;` for consistency. Otherwise, leave re-exports alone.

There are no other changes. The edit is purely additive, so existing references are unaffected.
