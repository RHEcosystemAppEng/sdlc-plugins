# File 2 (MODIFY): `modules/fundamental/src/advisory/model/mod.rs`

Register the new model module alongside the existing ones.

```diff
 pub mod details;
+pub mod severity_summary;
 pub mod summary;
```

If the file also re-exports sibling types (e.g. `pub use summary::*;`), add the matching line:

```diff
 pub use details::*;
+pub use severity_summary::*;
 pub use summary::*;
```

No other changes.
