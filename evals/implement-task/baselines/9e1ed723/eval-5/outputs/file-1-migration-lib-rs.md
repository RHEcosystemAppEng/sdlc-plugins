# File 1 (MODIFY): `migration/src/lib.rs`

## Purpose
Register the new migration so `Migrator` applies it after `m0001_initial`.

## Changes
1. Add a module declaration next to the existing one:
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```
2. Append the migration to the `vec![]` in `migrations()`, keeping chronological order:
```rust
#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m0001_initial::Migration),
            Box::new(m0002_drop_advisory_status::Migration),
        ]
    }
}
```

## Notes
- Follow the exact visibility used for `m0001_initial` (`mod` vs `pub mod`). Check this with `get_symbols_overview` first and mirror it.
- No other changes. Existing ordering is preserved, and since SeaORM records applied migrations by name, m0002 runs once on existing databases.
