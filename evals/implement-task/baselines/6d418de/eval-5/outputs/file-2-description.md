# File 2: `migration/src/lib.rs` (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so it is executed by the SeaORM migration runner.

## Sibling Analysis

The existing `lib.rs` follows this pattern:
- Module declarations at the top (e.g., `mod m0001_initial;`)
- A `Migrator` struct implementing `MigratorTrait`
- A `migrations()` function returning `Vec<Box<dyn MigrationTrait>>` with entries like `Box::new(m0001_initial::Migration)`

## Changes

### Change 1: Add module declaration

**Location**: After the existing `mod m0001_initial;` line

**Add**:
```rust
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the `migrations()` function

**Location**: Inside the `vec![]` in the `migrations()` function, after the `m0001_initial::Migration` entry

**Add**:
```rust
Box::new(m0002_drop_advisory_status::Migration),
```

## Expected Result

The `lib.rs` file will look like (showing relevant sections):

```rust
mod m0001_initial;
mod m0002_drop_advisory_status;

// ... Migrator struct ...

impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m0001_initial::Migration),
            Box::new(m0002_drop_advisory_status::Migration),
        ]
    }
}
```

## Rationale

- Migration ordering matters -- `m0002` must come after `m0001` in the vector to maintain correct execution order
- The module declaration follows alphabetical/numerical ordering consistent with the existing pattern
- No other changes to this file are needed
