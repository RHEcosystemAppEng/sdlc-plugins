# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration registry so SeaORM's migrator executes it.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module, alongside the existing `m0001_initial` declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function. It must come after `m0001_initial` to maintain execution order:

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

1. **Ordering**: The new migration is appended after `m0001_initial` to ensure correct sequential execution -- the `status` column must exist (created by `m0001_initial`) before it can be dropped
2. **Pattern conformance**: The registration follows the exact same `Box::new(module::Migration)` pattern used by `m0001_initial`
3. **No other changes**: Only the module declaration and the vec entry are added -- no other modifications to `lib.rs`
