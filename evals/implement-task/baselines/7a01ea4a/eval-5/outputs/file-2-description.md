# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration registry so that SeaORM's migration runner discovers and executes it.

## Pre-implementation Inspection

Read `migration/src/lib.rs` to understand:
- How `m0001_initial` is declared as a module (`mod m0001_initial;`)
- How the `migrations()` function is structured (returns a `Vec` of boxed migration trait objects)
- The exact syntax for adding entries to the `vec![]` (e.g., `Box::new(m0001_initial::Migration)`)
- Whether there is a `MigratorTrait` implementation or a standalone function

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

### Change 2: Register migration in the migrations list

Add the new migration to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry:

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

## Key Design Decisions

1. **Order matters**: The new migration is appended after `m0001_initial` in the `vec![]`. Migrations execute in the order they appear in this list, and `m0002` must run after `m0001` since `m0001` creates the table that `m0002` alters.

2. **Module naming convention**: The module name `m0002_drop_advisory_status` follows the established pattern of `m<number>_<descriptive_name>` seen in `m0001_initial`.

3. **No other changes**: Only the module declaration and vec entry are added. No other modifications to `lib.rs` are needed.

## Conventions Applied

- Module declarations ordered numerically (m0001, m0002, ...)
- Migration registration follows the same `Box::new(module::Migration)` pattern as existing entries
- No trailing comma style changes or formatting deviations from the existing code
