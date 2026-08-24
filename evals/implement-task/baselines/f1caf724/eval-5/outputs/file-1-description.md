# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration runner so it is executed when migrations are applied.

## Current State (from code inspection)

The file currently:
- Declares the `m0001_initial` module
- Contains a `migrations()` function that returns a `Vec<Box<dyn MigrationTrait>>` with `m0001_initial::Migration`

## Changes

### 1. Add module declaration

Add a new `mod` statement for the new migration module:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // NEW
```

### 2. Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, following the existing pattern:

```rust
pub fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // NEW
    ]
}
```

## Conventions followed

- Module declaration follows alphabetical/numerical ordering consistent with existing `m0001_initial`
- Registration pattern matches the existing `Box::new(...)` pattern in the `vec![]`
- No imports needed -- the migration struct is accessed via module path

## Verification

After modifying, use `mcp__serena_backend__find_symbol` on the `migrations` function to confirm both migrations are registered.
