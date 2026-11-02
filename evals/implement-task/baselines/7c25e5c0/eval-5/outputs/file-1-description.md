# File 1 (Modify): migration/src/lib.rs

## Purpose
Register the new migration module so it is included in the migration list.

## Changes

### 1. Add module declaration
Add the module declaration for the new migration at the top of the file, after the existing `m0001_initial` module:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // NEW
```

### 2. Register migration in migrations() function
Add the new migration to the `vec![]` returned by the `migrations()` function, after the `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // NEW
    ]
}
```

## Rationale
Following the existing registration pattern established by `m0001_initial`. The new migration is appended to the end of the list to ensure sequential execution order.
