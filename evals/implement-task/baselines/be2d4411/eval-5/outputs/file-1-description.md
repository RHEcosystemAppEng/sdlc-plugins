# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new migration module `m0002_drop_advisory_status` so that SeaORM's migration runner includes it when applying migrations.

## Current State (expected)

The file currently contains:
- A module declaration for `m0001_initial`
- A struct implementing `MigratorTrait` with a `migrations()` method
- The `migrations()` method returns a `vec![]` containing `Box::new(m0001_initial::Migration)`

## Changes

### 1. Add module declaration

Add a new module declaration after the existing one:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // NEW
```

### 2. Register migration in the migrations() function

Add the new migration to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // NEW
    ]
}
```

## Inspection Required Before Modifying

- Read the current contents of `migration/src/lib.rs` to confirm the exact structure and pattern used for registering migrations
- Verify the import style and any additional traits or macros used
