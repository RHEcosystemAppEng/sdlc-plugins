# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module in the migration runner so it is executed as part of the database migration sequence.

## Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, alongside the existing `m0001_initial` declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, after `m0001_initial`:

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

1. **Sequential ordering**: The new migration is added after `m0001_initial` in the vec, maintaining chronological order. SeaORM processes migrations in the order they appear in this list.

2. **Module declaration placement**: The `mod` declaration is placed immediately after `m0001_initial` to maintain alphabetical/sequential ordering of module declarations.

3. **Minimal change**: Only two lines are added -- one module declaration and one vec entry. No other modifications to `lib.rs` are needed.

## Conventions Followed

- Same `Box::new(<module>::Migration)` pattern as used for `m0001_initial`
- Module declarations at the top of the file
- Sequential ordering in the migrations vec matching the module numbering
