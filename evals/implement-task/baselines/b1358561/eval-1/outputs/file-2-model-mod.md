# File 2 (MODIFY): `modules/fundamental/src/advisory/model/mod.rs`

Register the new model module next to the existing ones, keeping alphabetical order:

```diff
 pub mod details;
+pub mod severity_summary;
 pub mod summary;
```

If siblings re-export (e.g. `pub use summary::*;`), add the matching
`pub use severity_summary::*;` line in the same style.
