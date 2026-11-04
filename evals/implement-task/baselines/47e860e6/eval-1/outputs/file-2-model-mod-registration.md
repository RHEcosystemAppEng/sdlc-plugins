# File 2 — MODIFY `modules/fundamental/src/advisory/model/mod.rs`

Register the new model module alongside the existing `summary` and `details` modules (keep alphabetical order used by siblings).

```diff
 pub mod details;
+pub mod severity_summary;
 pub mod summary;
```

If the sibling `mod.rs` also re-exports types (e.g. `pub use summary::*;`), add the matching `pub use severity_summary::*;` for consistency.
