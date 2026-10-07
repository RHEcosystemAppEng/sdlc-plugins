# File 2: Modify `migration/src/lib.rs`

## Action: MODIFY

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration registry so it is discovered and executed by SeaORM's migration runner.

## Pre-implementation inspection

Before modifying this file, read `migration/src/lib.rs` to understand:
- How migration modules are declared (e.g., `mod m0001_initial;`)
- How the `migrations()` function is structured
- The `vec![]` pattern for listing migrations
- The struct that implements `MigratorTrait`

## Detailed changes

### Change 1: Add module declaration

Add a new module declaration for the migration, following the existing pattern:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`:

```rust
// Existing pattern (example):
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        // Add:
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new migration is appended after `m0001_initial` to maintain chronological ordering.

## Conventions followed

- Module declaration follows alphabetical/numerical ordering
- Migration registration follows the `Box::new(module::Migration)` pattern
- Chronological ordering maintained (m0002 after m0001)
