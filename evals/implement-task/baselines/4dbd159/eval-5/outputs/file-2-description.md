# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration list so that the SeaORM migrator discovers and runs it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing `m0001_initial` module.

**Before:**
```rust
mod m0001_initial;
```

**After:**
```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial` entry. Migrations are executed in the order they appear in this vector, so the new entry must come after m0001_initial.

**Before:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}
```

**After:**
```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Key Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` to maintain chronological ordering. The `m0002_` prefix in the module name also reflects this ordering convention.
2. **Pattern conformance**: Follows the exact same `Box::new(<module>::Migration)` pattern used by the existing entry.
