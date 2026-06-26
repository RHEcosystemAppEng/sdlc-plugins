# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is executed as part of the migration sequence.

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, following the existing `m0001_initial` declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

**Rationale**: Rust requires explicit module declarations. The module name matches the directory name `m0002_drop_advisory_status/` which contains `mod.rs`.

### Change 2: Register the migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function. It must come after `m0001_initial` to maintain correct migration ordering:

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

**Rationale**: SeaORM runs migrations in the order they appear in this vector. Since m0002 drops a column that m0001 may have created, m0002 must come after m0001. The pattern follows exactly how m0001_initial is registered.

## Pre-Modification Inspection

Before making these changes, the following would be verified:

1. **Read `migration/src/lib.rs`** via `mcp__serena_backend__get_symbols_overview` to see the current structure -- confirming the `migrations()` function exists and understanding the exact `vec![]` pattern used
2. **Verify the module declaration style** -- confirm whether `mod m0001_initial;` uses `pub mod` or `mod` and match accordingly
3. **Check for any additional boilerplate** -- e.g., re-exports, use statements, or trait implementations in lib.rs that may need updating

## Scope

These are minimal, targeted changes:
- One new `mod` line
- One new `Box::new(...)` entry in an existing vector
- No changes to existing logic, signatures, or behavior
