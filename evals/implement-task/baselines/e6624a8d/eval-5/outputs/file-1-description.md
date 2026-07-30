# File 1: migration/src/lib.rs (MODIFY)

## Purpose
Register the new migration module so the migration runner discovers and executes it.

## Changes

### 1. Add module declaration
Add a new `mod` statement alongside the existing `m0001_initial` module declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### 2. Register migration in the `migrations()` function
Add the new migration to the `vec![]` inside the `migrations()` function, after the existing `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Rationale
- The module declaration makes Rust aware of the new migration subdirectory
- The `migrations()` registration tells the migration runner to include this migration in the execution sequence
- Ordering after `m0001_initial` ensures the migration runs in the correct sequence (the `advisory` table must exist before its column can be dropped)

## Convention Compliance
- Follows the same registration pattern used by `m0001_initial`
- Module naming matches the directory name `m0002_drop_advisory_status`
- Uses `Box::new(...)` wrapping consistent with existing migrations
