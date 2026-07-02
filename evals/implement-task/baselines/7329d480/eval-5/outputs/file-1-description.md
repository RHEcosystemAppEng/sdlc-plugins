# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it runs as part of the migration sequence.

## Changes

### 1. Add module declaration

Add a new `mod` declaration for the migration module alongside the existing one:

```rust
// Existing:
mod m0001_initial;

// Add:
mod m0002_drop_advisory_status;
```

### 2. Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function. It must appear after `m0001_initial` since migrations run in order:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- add this line
    ]
}
```

## Rationale

The migration runner discovers migrations through this registry. Without adding the module declaration and the entry in the `migrations()` vec, the new migration file would exist but never execute.

## Convention Conformance

This follows the exact pattern established by `m0001_initial` -- each migration is declared as a module and registered as a boxed `Migration` struct in the migrations vector.
