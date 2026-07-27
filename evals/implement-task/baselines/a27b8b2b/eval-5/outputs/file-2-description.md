# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration list so it is executed by the migration runner.

## Pre-Implementation Inspection

Before modifying this file, inspect it using Serena (`mcp__serena_backend__get_symbols_overview` on `migration/src/lib.rs`) or Read to understand:
- The existing module declarations (`mod m0001_initial;`)
- The `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>`
- The ordering of migrations in the vec (must be appended at the end)

## Detailed Changes

### Change 1: Add module declaration

Add a new module declaration for the migration directory:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register the migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function:

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

## Conventions Applied

- Module declaration follows the same pattern as `m0001_initial` (simple `mod` statement)
- Migration registration follows the `Box::new(module::Migration)` pattern used by m0001_initial
- New migration is appended at the end of the vec to ensure correct execution order
- No other changes to the file; scope is strictly limited to registration
