# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner includes it when running pending migrations.

## Current state (expected)

The file currently:
1. Declares `mod m0001_initial;`
2. Implements a `MigratorTrait` or similar that returns a `migrations()` function
3. The `migrations()` function returns a `vec![]` containing `Box::new(m0001_initial::Migration)`

## Changes

### 1. Add module declaration

Add the following line after the existing `mod m0001_initial;` declaration:

```rust
mod m0002_drop_advisory_status;
```

### 2. Register migration in migrations() function

Add the new migration to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry:

```rust
Box::new(m0002_drop_advisory_status::Migration),
```

## Expected result after modification

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;

// ... (existing code)

fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Rationale

Following the existing pattern established by `m0001_initial` registration. Migrations must be registered in sequential order to ensure they run in the correct sequence.
