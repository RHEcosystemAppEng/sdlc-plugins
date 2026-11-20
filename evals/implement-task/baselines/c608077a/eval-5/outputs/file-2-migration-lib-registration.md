# File 2 (MODIFY): `migration/src/lib.rs`

Purpose: register the new migration so SeaORM's `Migrator` applies it after `m0001_initial`.

## Changes

1. Add the module declaration next to the existing one:

```diff
 pub use sea_orm_migration::prelude::*;

 mod m0001_initial;
+mod m0002_drop_advisory_status;
```

2. Append the migration to the `vec![]` in `migrations()`, after `m0001_initial` (order is
   significant — migrations run in vec order):

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

Edit method: `mcp__serena_backend__replace_symbol_body` on `migrations` (or `insert_after_symbol`
for the `mod` line), falling back to Edit. Exact surrounding lines are matched to whatever
`get_symbols_overview` / `find_symbol(include_body=true)` shows; the diff above reflects the
standard SeaORM layout described by the task's Implementation Notes.

No other changes to this file. Backward compatibility: `migrations()` callers
(`Migrator::up/down`, server startup) are unaffected except for the new step.
