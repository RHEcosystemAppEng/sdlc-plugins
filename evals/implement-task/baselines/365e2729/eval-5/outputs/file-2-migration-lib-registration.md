# File 2 (Modify): `migration/src/lib.rs`

Register the new migration following the existing `m0001_initial` pattern.

## Changes

1. Add the module declaration next to the existing one:

```diff
 pub use sea_orm_migration::prelude::*;

 mod m0001_initial;
+mod m0002_drop_advisory_status;
```

2. Append the migration to the `vec![]` in `migrations()`, after `m0001_initial` (ordering
   matters — migrations run in vec order):

```diff
 #[async_trait::async_trait]
 impl MigratorTrait for Migrator {
     fn migrations() -> Vec<Box<dyn MigrationTrait>> {
         vec![
             Box::new(m0001_initial::Migration),
+            Box::new(m0002_drop_advisory_status::Migration),
         ]
     }
 }
```

## Notes

- The exact surrounding code (e.g. whether `vec![...]` is single-line) would be confirmed via
  `mcp__serena_backend__find_symbol("Migrator/migrations", include_body=true)` and the
  edit applied with `replace_symbol_body` / matching formatting; `cargo fmt` keeps style
  consistent.
- No other symbols in `lib.rs` change; `Migrator` callers (server startup, tests) are
  unaffected — verified with `find_referencing_symbols("Migrator")`.
