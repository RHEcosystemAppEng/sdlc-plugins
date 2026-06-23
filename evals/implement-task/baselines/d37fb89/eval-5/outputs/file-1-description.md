# File 1: migration/src/lib.rs (MODIFY)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration registry so that SeaORM's migration runner discovers and executes it.

## Current State (expected)

The file currently contains:
- A `mod m0001_initial;` module declaration
- A struct implementing `MigratorTrait` with a `migrations()` method
- The `migrations()` method returns a `Vec<Box<dyn MigrationTrait>>` containing `Box::new(m0001_initial::Migration)`

## Changes

### 1. Add module declaration

Add the new module declaration alongside the existing one:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // NEW
```

### 2. Register migration in migrations() function

Add the new migration to the `vec![]` returned by `migrations()`, after the existing `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // NEW
    ]
}
```

## Conventions Followed

- Migration modules are listed in chronological order (m0001, m0002, ...)
- Each migration is boxed as `Box::new(<module>::Migration)`
- Module names use the pattern `m<NNNN>_<descriptive_name>`

## Verification

- The new migration must appear after `m0001_initial` in the vector to ensure correct execution order
- The module name `m0002_drop_advisory_status` must match the directory name exactly
- `cargo build` must pass after this change (combined with the new module file)
