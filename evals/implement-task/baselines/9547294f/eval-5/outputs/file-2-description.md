# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it runs as part of the migration sequence.

## Detailed Changes

### Change 1: Add module declaration

Add the module declaration for the new migration at the top of the file, after the existing `m0001_initial` declaration:

```rust
// BEFORE:
mod m0001_initial;

// AFTER:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function in the `MigratorTrait` implementation, after the existing `m0001_initial` entry:

```rust
// BEFORE:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// AFTER:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

### Design Decisions

1. **Sequential ordering**: The new migration is added after `m0001_initial` to maintain chronological execution order — SeaORM runs migrations in the order they appear in the vector.
2. **Naming consistency**: The module name `m0002_drop_advisory_status` follows the established `m<NNNN>_<descriptive_name>` pattern, incrementing the sequence number from `m0001`.
3. **No other changes**: Only the module declaration and vec registration are modified — no other code in `lib.rs` is touched, keeping changes scoped to exactly what the task requires.
