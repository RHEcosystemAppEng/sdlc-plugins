# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migrator discovers and executes it.

## Detailed Changes

### Change 1: Add module declaration

Add the module declaration for the new migration alongside the existing one:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register in migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, appended after the existing `m0001_initial` entry:

```rust
// Before:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// After:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Key Design Decisions

1. **Ordering**: The new migration is appended at the end of the `vec![]`, after `m0001_initial`. SeaORM executes migrations in the order they appear in this vector, so the initial schema must be created before we attempt to drop a column from it.
2. **Module naming**: Uses `m0002_drop_advisory_status` following the existing `m0001_initial` numbering convention with a descriptive suffix.

### Conventions Followed

- Follows the existing pattern of `Box::new(<module>::Migration)` entries in the migrations vector
- Module declaration placed in alphabetical/numerical order after existing declarations
- Migration order in the vector matches the chronological sequence of schema changes
