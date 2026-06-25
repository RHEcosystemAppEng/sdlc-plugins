# File 2: `migration/src/lib.rs` (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner includes it when running migrations.

## Detailed Changes

### Change 1: Add module declaration

Add a `mod` declaration for the new migration module alongside the existing `m0001_initial`:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // ADD THIS LINE
```

### Change 2: Register migration in the `migrations()` function

Add the new migration to the `vec![]` inside the `migrations()` function, following the pattern of `m0001_initial`:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // ADD THIS LINE
    ]
}
```

## Key Implementation Details

- The new migration is appended after `m0001_initial` in the vector, maintaining chronological ordering. Migration order matters -- SeaORM executes them sequentially.
- The module path `m0002_drop_advisory_status` matches the directory name `migration/src/m0002_drop_advisory_status/`.
- The `::Migration` suffix references the `Migration` struct defined in the new module's `mod.rs`.
