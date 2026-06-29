# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration list so SeaORM's migration runner discovers and executes it.

## Detailed Changes

### 1. Add module declaration

Add a `mod` declaration for the new migration module alongside the existing `m0001_initial`:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // ADD this line
```

### 2. Register in migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, placing it after `m0001_initial` to ensure correct execution order:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // ADD this line
    ]
}
```

### Key Decisions

- **Ordering**: The new migration is appended after `m0001_initial` in the vec, maintaining chronological order. SeaORM executes migrations in the order they appear in this list.
- **Pattern conformance**: The registration follows exactly the same pattern as `m0001_initial` -- `Box::new(<module>::Migration)` -- consistent with the sibling convention.
- **No other changes**: Only the module declaration and vec entry are added; no other modifications to `lib.rs` are needed.
