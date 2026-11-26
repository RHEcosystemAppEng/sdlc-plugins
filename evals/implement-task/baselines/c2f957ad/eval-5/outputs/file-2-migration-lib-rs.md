# File 2 (MODIFY): `migration/src/lib.rs`

Goal: register the new migration, following the `m0001_initial` pattern.

## Change 1: module declaration

Add it right after the existing `mod m0001_initial;`:

```diff
 pub use sea_orm_migration::prelude::*;

 mod m0001_initial;
+mod m0002_drop_advisory_status;
```

## Change 2: add to the `migrations()` vec, in order after m0001

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
- The surrounding code shown above is what a standard SeaORM `Migrator` looks like. The exact existing text would be confirmed with `find_symbol("Migrator/migrations", include_body=true)` before editing, and edited with Serena `replace_symbol_body` (or Edit as a fallback).
- Ordering matters: m0002 must come after m0001 because it alters a table that m0001 creates.
- No other changes to this file.
