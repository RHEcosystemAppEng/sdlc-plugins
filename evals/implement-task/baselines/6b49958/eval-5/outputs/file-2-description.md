# File 2: migration/src/lib.rs (MODIFY)

## Purpose

Register the new `m0002_drop_advisory_status` migration module so that SeaORM's migration runner includes it when running migrations.

## Detailed Changes

### Change 1: Add module declaration

Add a new `mod` declaration for the migration module, placed after the existing `m0001_initial` module declaration:

```rust
// Before:
mod m0001_initial;

// After:
mod m0001_initial;
mod m0002_drop_advisory_status;
```

### Change 2: Register migration in the migrations() function

Add the new migration to the `vec![]` returned by the `migrations()` function, after the existing `m0001_initial::Migration` entry:

```rust
// Before:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
    ]
}

// After:
fn migrations() -> Vec<Box<dyn MigrationTrait>> {
    vec![
        Box::new(m0001_initial::Migration),
        Box::new(m0002_drop_advisory_status::Migration),
    ]
}
```

## Conventions Applied

- Module declarations are ordered sequentially by migration number
- Migrations are registered in the `vec![]` in the same sequential order
- Each migration is wrapped in `Box::new()` to satisfy the `Box<dyn MigrationTrait>` return type
- The trailing comma convention follows whatever the existing code uses (determined during code inspection of the actual file)
