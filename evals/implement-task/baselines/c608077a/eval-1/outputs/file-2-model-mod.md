# File 2 — MODIFY `modules/fundamental/src/advisory/model/mod.rs`

Register the new model module alongside existing `summary` and `details`.

```diff
 pub mod details;
+pub mod severity_summary;
 pub mod summary;
```

If the existing `mod.rs` re-exports sibling types (e.g. `pub use summary::*;`), add the matching line to stay consistent:

```diff
 pub use details::*;
+pub use severity_summary::*;
 pub use summary::*;
```

Alphabetical ordering preserved per sibling layout.
