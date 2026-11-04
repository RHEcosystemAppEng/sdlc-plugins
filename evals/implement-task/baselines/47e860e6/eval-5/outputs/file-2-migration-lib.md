# File 2 (MODIFY): `migration/src/lib.rs`

Listed in the task's **Files to Modify**. The change registers the new migration module in the `migrations()` list, following the `m0001_initial` pattern.

## Expected current shape (would confirm with `mcp__serena_backend__get_symbols_overview` / `find_symbol`)

```rust
pub use sea_orm_migration::prelude::*;

mod m0001_initial;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![Box::new(m0001_initial::Migration)]
    }
}
```

## Changes

1. Add the module declaration directly after `mod m0001_initial;`:

```diff
 mod m0001_initial;
+mod m0002_drop_advisory_status;
```

2. Append the migration to the vec, after m0001. SeaORM applies migrations in vector order, so m0002 must come last:

```diff
     fn migrations() -> Vec<Box<dyn MigrationTrait>> {
-        vec![Box::new(m0001_initial::Migration)]
+        vec![
+            Box::new(m0001_initial::Migration),
+            Box::new(m0002_drop_advisory_status::Migration),
+        ]
     }
```

No other changes. Run `cargo fmt` so the multi-line vec formatting matches rustfmt.
