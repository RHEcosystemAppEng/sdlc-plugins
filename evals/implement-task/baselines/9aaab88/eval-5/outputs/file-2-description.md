# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is executed by the migration runner.

## Detailed Changes

### 1. Add module declaration

Add a `mod` declaration for the new migration module alongside the existing one:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### 2. Register in migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the existing `m0001_initial` entry pattern:

```rust
fn migrations(&self) -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // Add this line
    ]
}
```

### Key Design Decisions

1. **Ordering**: The new migration is appended after `m0001_initial` to ensure correct execution order. Migrations run sequentially in the order they appear in the vec.
2. **Follows sibling pattern**: The registration follows the exact same pattern as `m0001_initial` -- `Box::new(<module>::Migration)` added to the vec.
3. **Module declaration**: The `mod` statement is placed alongside the existing module declarations at the top of the file.
