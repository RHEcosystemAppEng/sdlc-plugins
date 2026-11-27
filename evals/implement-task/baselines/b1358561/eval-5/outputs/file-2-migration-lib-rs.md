# File 2 (MODIFY): `migration/src/lib.rs`

Purpose: register the new migration in the ordered migration list.

Changes:
1. Add the module declaration after the existing one:
```diff
 pub use sea_orm_migration::prelude::*;

 mod m0001_initial;
+mod m0002_drop_advisory_status;
```
2. Append the migration to `migrations()`, preserving order (m0001 first, then m0002):
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

There are no other changes. Edit method: `mcp__serena_backend__replace_symbol_body` on `Migrator/migrations`, and `insert_after_symbol` (or Edit) for the `mod` line.
