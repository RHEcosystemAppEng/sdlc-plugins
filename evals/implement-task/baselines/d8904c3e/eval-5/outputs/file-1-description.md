# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new migration module `m0002_drop_advisory_status` in the migration list so that SeaORM's migration runner executes it.

## Current State (Expected)

The file currently declares the `m0001_initial` module and returns it in a `migrations()` function that implements SeaORM's `MigratorTrait`. The pattern looks like:

```rust
mod m0001_initial;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m0001_initial::Migration),
        ]
    }
}
```

## Changes

### 1. Add module declaration

Add a new `mod` statement for the new migration module, placed after the existing `m0001_initial` declaration:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### 2. Register the migration in the migrations() vector

Add the new migration to the `vec![]` in the `migrations()` function, after `m0001_initial::Migration`, following the same `Box::new(...)` pattern:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- Follow the exact same pattern as `m0001_initial` registration (module declaration + Box::new in vec)
- Maintain ordering: migrations must be listed in chronological order (m0001 before m0002)
- Use trailing comma after the last entry in the vec (if existing code follows this pattern)

## Verification

- The file must compile without errors (`cargo check -p migration`)
- The `Migrator::migrations()` function must return both migrations in order
