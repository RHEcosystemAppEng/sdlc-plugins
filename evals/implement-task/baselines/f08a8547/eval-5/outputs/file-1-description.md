# File 1: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration runner so it is executed when migrations are applied.

## Current State (Expected)

The file currently:
- Declares `mod m0001_initial;`
- Contains a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>`
- The vec contains `Box::new(m0001_initial::Migration)`

## Changes

### 1. Add module declaration

Add a new module declaration after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- ADD THIS LINE
```

### 2. Register migration in the migrations function

Add the new migration to the `vec![]` in the `migrations()` function, after the m0001_initial entry. Order matters -- migrations run sequentially:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- ADD THIS LINE
    ]
}
```

## Rationale

The migration runner iterates the vector returned by `migrations()` to determine which migrations to apply. Without registration here, the new migration module would exist on disk but never execute.

## Verification

- Confirm the new entry is placed after `m0001_initial` (ordering is sequential)
- Confirm the module path matches the directory name exactly: `m0002_drop_advisory_status`
- Confirm the struct name matches what is exported from the new module: `Migration`
