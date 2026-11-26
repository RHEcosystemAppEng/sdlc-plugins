# File 4 (MODIFY): `modules/fundamental/src/advisory/model/mod.rs`

Register the new model module alongside the existing ones.

```diff
 pub mod details;
+pub mod severity_summary;
 pub mod summary;
```

Notes:
- Keep the existing ordering convention (alphabetical, as with `details`/`summary`).
- If the file re-exports siblings (`pub use summary::*;`), add the matching `pub use severity_summary::*;`
  for parity; otherwise no re-export.
