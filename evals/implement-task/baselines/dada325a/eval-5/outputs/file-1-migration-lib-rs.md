# File 1 — `migration/src/lib.rs` (MODIFY)

## Purpose
Register the new migration module so that `Migrator` applies it after `m0001_initial`.

## Changes

### 1. Add the module declaration
Add it next to the existing `mod m0001_initial;`, keeping the declarations in numeric order:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

(If the existing file uses `pub mod` for `m0001_initial`, use `pub mod` here too to match.)

### 2. Append to the `migrations()` vector
Inside `impl MigratorTrait for Migrator`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new migration is appended at the end, after `m0001_initial`, because SeaORM applies migrations in vector order and this one depends on the `advisory` table created by m0001.

## Not changed
- `Migrator` struct, `use` statements, and any other items stay the same.
- No new dependencies in `migration/Cargo.toml`, because `sea-orm-migration` is already used by m0001.
