# File 2: migration/src/lib.rs (MODIFY)

## Purpose
Register the new `m0002_drop_advisory_status` migration module so SeaORM discovers and runs it.

## Detailed Changes

### Add module declaration

Add the module declaration for the new migration, following the existing pattern:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### Register in migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing m0001_initial entry:

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

### Key decisions
- The new migration is appended at the end of the `vec![]` to maintain sequential execution order
- The pattern matches exactly how `m0001_initial` is registered -- `Box::new(<module>::Migration)`
- No other changes to lib.rs are needed
