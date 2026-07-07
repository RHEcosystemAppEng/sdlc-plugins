# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is discovered and
executed by SeaORM's migration runner.

## Pre-modification Inspection

Before modifying this file, inspect it to understand:
1. How existing migration modules are declared (e.g., `mod m0001_initial;`)
2. How the `migrations()` function is structured and where new entries are appended
3. The ordering convention (migrations are listed in chronological order)

## Detailed Changes

### Change 1: Add module declaration

Add a new module declaration for the migration, following the existing pattern:

```rust
// Existing:
mod m0001_initial;

// Add after:
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function:

```rust
// Existing (approximate structure):
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        // Add the following line:
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

The new entry is appended at the end of the vec, after all existing migrations, to
maintain chronological ordering. SeaORM executes migrations in the order they appear
in this list, so correct ordering is critical.

## Verification

After modification, verify:
- The module declaration compiles (`cargo check` in the migration crate)
- The migration appears in the correct position (after m0001_initial)
- No duplicate entries exist
