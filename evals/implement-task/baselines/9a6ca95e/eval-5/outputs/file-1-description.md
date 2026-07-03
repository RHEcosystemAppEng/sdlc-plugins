# File 1: migration/src/lib.rs (Modify)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is executed by the SeaORM migration runner.

## Pre-Implementation Inspection

Before modifying this file, read it using Serena (`mcp__serena_backend__get_symbols_overview`) or the Read tool to:
- Confirm the existing `mod m0001_initial;` declaration pattern
- Locate the `migrations()` function and its `vec![]` contents
- Understand the import structure and any trait bounds

## Changes

### 1. Add module declaration

Add a new module declaration for the migration, following the existing pattern:

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;  // <-- add this line
```

### 2. Register migration in the migrations vector

In the `migrations()` function, add the new migration to the `vec![]` after the existing `m0001_initial` entry:

```rust
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),  // <-- add this line
    ]
}
```

## Conventions Applied

- Follow the exact pattern of how `m0001_initial` is declared and registered
- Maintain alphabetical/sequential ordering of migration modules
- Use `Box::new(...)` wrapping consistent with the existing entry
